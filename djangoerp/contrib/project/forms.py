#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.forms import ModelForm
#rom django.utils.translation import ugettext_lazy as _
#rom django.core.exceptions import ValidationError

from .models import Project


class ProjectUpdateForm(ModelForm):
    class Meta:
        model = Project
        exclude = []
