#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.forms import ModelForm
# from django.utils.translation import ugettext_lazy as _
# from django.core.exceptions import ValidationError

from .models import Project


class ProjectUpdateForm(ModelForm):
    class Meta:
        model = Project
        exclude = []
