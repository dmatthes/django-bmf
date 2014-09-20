#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.db import models

from djangobmf.models import BMFModel


class WorkspaceTest(BMFModel):
    """
    """
    boolean = models.BooleanField(default=False)
