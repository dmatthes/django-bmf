#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals


from django import forms

from ..models import Watch


class WatchDefaultForm(forms.ModelForm):

    class Meta:
        model = Watch
        fields = ['new_entry', 'comment', 'file', 'changed', 'workflow']

#   def __init__(self, *args, **kwargs):
#       super(WatchDefaultForm, self).__init__(*args, **kwargs)
#       field = self.fields.get('topic')
#       field.widget = forms.TextInput(attrs={'placeholder': field.label, 'class': 'form-control'})

#       field = self.fields.get('text')
#       field.widget = forms.Textarea(attrs={'rows': 8, 'class': 'form-control'})


class WatchObjectForm(forms.ModelForm):

    class Meta:
        model = Watch
        fields = ['comment', 'file', 'changed', 'workflow']

#   def __init__(self, *args, **kwargs):
#       super(HistoryCommentForm, self).__init__(*args, **kwargs)
#       field = self.fields.get('topic')
#       field.widget = forms.TextInput(attrs={'placeholder': field.label, 'class': 'form-control'})

#       field = self.fields.get('text')
#       field.widget = forms.Textarea(attrs={'rows': 8, 'class': 'form-control'})
