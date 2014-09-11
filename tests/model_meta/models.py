#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.db import models

from djangobmf.models import BMFModel

class Category(BMFModel):
    field1 = models.BooleanField(default=True)

    class BMFMeta:
        category = "SALES"
