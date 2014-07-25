#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.db import models
# from django.utils.translation import ugettext_lazy as _

from djangoerp.settings import BASE_MODULE
from djangoerp.file.models import BaseDocument


class AbstractDocument(BaseDocument):
    if BASE_MODULE["CUSTOMER"]:
        customer = models.ForeignKey(
            BASE_MODULE["CUSTOMER"], null=True, blank=True, on_delete=models.SET_NULL,
        )
    if BASE_MODULE["PROJECT"]:
        project = models.ForeignKey(
            BASE_MODULE["PROJECT"], null=True, blank=True, on_delete=models.SET_NULL,
        )

    class Meta(BaseDocument.Meta):
        abstract = True


class Document(AbstractDocument):
    pass
