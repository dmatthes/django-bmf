#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.forms import ModelForm
from django.forms import TextInput
from django.forms import HiddenInput
from django.utils.translation import ugettext_lazy as _

from .models import View


class ViewForm(ModelForm):
    class Meta:
        model = View
        fields = ['dashboard', 'category', 'name', 'url', 'kwargs', 'search']

    def __init__(self, *args, **kwargs):
        super(ViewForm, self).__init__(*args, **kwargs)

        field = self.fields.get('dashboard')
        field.widget.attrs.update({
            'class': 'form-control',
        })
        field.empty_label = _("Select Dashboard")

        field = self.fields.get('category')
        field.widget = TextInput(attrs={'placeholder': field.label, 'class': 'form-control'})

        field = self.fields.get('name')
        field.widget = TextInput(attrs={'placeholder': field.label, 'class': 'form-control'})

        for name in ['url', 'kwargs', 'search']:
            field = self.fields.get(name)
            field.widget = HiddenInput()

