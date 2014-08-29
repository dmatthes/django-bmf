#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from djangoerp.forms import ERPForm

from .models import Goal


class GoalCloneForm(ModelForm):
    class Meta:
        model = Goal
        exclude = []
    copy_tasks = forms.BooleanField(label=_("Copy the Tasks"), initial=True, required=False)
    clear_employee = forms.BooleanField(label=_("When copying unset the task's employee"), initial=True, required=False)


class ERPGoalCloneForm(ERPForm):
    class Meta:
        form_class = GoalCloneForm
