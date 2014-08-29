#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.db.models import get_models
from django.db.models.signals import post_syncdb
from django.contrib.contenttypes.models import ContentType

from . import models as bmfcore
from .numbering.models import NumberCycle


def install(sender, created_models, **kwargs):
    for model in get_models():  # TODO change to django.apps
        if getattr(model, 'BMFMeta', False):

            kwargs = {
                'app_label': model._meta.app_label,
                'model': model._meta.model_name,
            }

            # LOOK: maybe we could move this to a signal
            try:
                ct = ContentType.objects.get(**kwargs)
            except ContentType.DoesNotExist:
                ct = ContentType(**kwargs)
                ct.name = model._meta.verbose_name_raw
                ct.save()

            if model._bmfmeta.number_cycle:
                count = NumberCycle.objects.filter(ct=ct).count()
                if not count:
                    obj = NumberCycle(ct=ct, name_template=model._bmfmeta.number_cycle)
                    obj.save()
    return None

post_syncdb.connect(install, sender=bmfcore, dispatch_uid="install_djangobmf_modules")
