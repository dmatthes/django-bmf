#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django import forms

# from djangobmf.documents.widgets import FileWidget

from .models import Document


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        exclude = []
        # widgets = {
        #     'file': FileWidget(),
        # }
