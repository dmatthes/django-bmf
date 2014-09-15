#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.forms import ModelForm

from .models import Timesheet


class TimesheetCreateForm(ModelForm):
    class Meta:
        model = Timesheet
        exclude = [
            'start',
            'end',
        ]


class TimesheetUpdateForm(ModelForm):
    class Meta:
        model = Timesheet
        exclude = [
        ]
