#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from django.utils.text import get_valid_filename
from django.utils.timezone import now
from django.utils.encoding import force_text, smart_str
from django.utils.encoding import python_2_unicode_compatible

from .storage import ERPStorage

from ..modelbase import ERPModel
from ..categories import DOCUMENT
from ..settings import STORAGE_STATIC_PREFIX

import uuid
import os


def generate_filename(instance, filename):
    prefix = []
    if instance.is_static:
        prefix.append(STORAGE_STATIC_PREFIX)
        if instance.content_type:
            prefix.append('%s' % instance.content_type.name)
            if instance.content_id:
                prefix.append('%s' % instance.content_id)
    else:
        uuid_str = str(uuid.uuid4())
        prefix.append(force_text(now().strftime(smart_str("%Y"))))
        prefix.append(force_text(now().strftime(smart_str("%m"))))
        prefix.append(uuid_str[0:2])
        prefix.append(uuid_str[2:4])
        prefix.append(uuid_str[4:])
    prefix.append(get_valid_filename(filename))
    return os.path.join(*prefix)


@python_2_unicode_compatible
class BaseDocument(ERPModel):
    file = models.FileField(_('File'), upload_to=generate_filename, storage=ERPStorage())
    size = models.PositiveIntegerField(null=True, blank=True, editable=False)

    is_static = models.BooleanField(default=False)

    content_type = models.ForeignKey(ContentType, related_name="erp_document", null=True, blank=True, editable=False, on_delete=models.SET_NULL)
    content_id = models.PositiveIntegerField(null=True, blank=True, editable=False)
    content_object = GenericForeignKey('content_type', 'content_id')

    class Meta:
        verbose_name = _('Document')
        verbose_name_plural = _('Documents')
        get_latest_by = "modified"
        abstract = True

    def __str__(self):
        return '%s' % self.file.name.split(r'/')[-1]

    def clean(self):
        if self.file:
            self.size = self.file.size

        if hasattr(self, 'project') and hasattr(self.content_object, 'erpget_project'):
            self.project = self.content_object.get_project

        if hasattr(self, 'customer') and hasattr(self.content_object, 'erpget_customer'):
            self.customer = self.content_object.get_customer

    class ERPMeta:
        category = DOCUMENT
        has_history = False
        has_file = False
