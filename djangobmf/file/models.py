#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from .storage import ERPStorage

from ..categories import DOCUMENT
from ..utils import generate_filename
from ..modelbase import ERPModel


@python_2_unicode_compatible
class BaseDocument(ERPModel):
    file = models.FileField(_('File'), upload_to=generate_filename, storage=ERPStorage())
    size = models.PositiveIntegerField(null=True, blank=True, editable=False)

    is_static = models.BooleanField(default=False)

    content_type = models.ForeignKey(
        ContentType,
        related_name="erp_document",
        null=True,
        blank=True,
        editable=False,
        on_delete=models.SET_NULL,
    )
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

    @models.permalink
    def erpfile_download(self):
        """
        A permalink to the default view of this model in the ERP-System
        """
        return ('djangoerp:file_download', (), {"pk": self.pk})
