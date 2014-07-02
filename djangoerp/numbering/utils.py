#/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType

import re

from .models import NumberCycle
from .validators import match_y


def numbercycle_get_name(object):
    model = object._meta.model
    ct = ContentType.objects.get_for_model(model)
    nc = NumberCycle.objects.get(ct=ct)
    return nc.generate_name(model, object)


def numbercycle_delete_object(object):
    model = object._meta.model
    ct = ContentType.objects.get_for_model(model)
    nc = NumberCycle.objects.get(ct=ct)

    if not bool(re.findall(match_y, nc.name_template)):
        return None # do nothing

    start, end = nc.get_periods()
    if end < object.created:
        return None # do nothing

    nc.counter_start += 1
    nc.save()
