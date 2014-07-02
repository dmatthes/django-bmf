#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

from .models import Position


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        exclude = []

    def __init__(self, *args, **kwargs):
        super(PositionForm, self).__init__(*args, **kwargs)
