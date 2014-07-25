#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django import forms

from .models import Position


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        exclude = []

    def __init__(self, *args, **kwargs):
        super(PositionForm, self).__init__(*args, **kwargs)
