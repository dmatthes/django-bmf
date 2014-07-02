#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Activity


class HistoryCommentForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['topic', 'text']

    def __init__(self, *args, **kwargs):
        super(HistoryCommentForm, self).__init__(*args, **kwargs)
        field = self.fields.get('topic')
        field.widget = forms.TextInput(attrs={'placeholder': field.label, 'class': 'form-control'})

        field = self.fields.get('text')
        field.widget = forms.Textarea(attrs={'rows': 8, 'class': 'form-control'})


class FollowForm(forms.Form):
    new_entry = forms.BooleanField(required=False, initial=False)
    glob_comment = forms.BooleanField(required=False, initial=False)
    glob_file = forms.BooleanField(required=False, initial=False)
    glob_changed = forms.BooleanField(required=False, initial=False)
    glob_workflow = forms.BooleanField(required=False, initial=False)
    comment = forms.BooleanField(required=False, initial=False)
    file = forms.BooleanField(required=False, initial=False)
    changed = forms.BooleanField(required=False, initial=False)
    workflow = forms.BooleanField(required=False, initial=False)

