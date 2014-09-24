from django import forms

from .models import Document


class UploadDocument(forms.ModelForm):

    class Meta:
        model = Document
        fields = ['file']
