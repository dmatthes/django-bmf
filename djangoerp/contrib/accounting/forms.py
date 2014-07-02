#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from djangoerp.forms import ERPForm

from .models import Transaction, TransactionItem


class TransactionUpdateForm(ModelForm):
    class Meta:
        model = Transaction
        exclude = []


class TransactionCreateForm(ModelForm):
    class Meta:
        model = Transaction
        exclude = []

TransactionInlineFormset = inlineformset_factory(Transaction, TransactionItem, extra=3, exclude=[])


class ERPTransactionUpdateForm(ERPForm):
    class Meta:
        form_class = TransactionUpdateForm
        inlines = {'accounts': TransactionInlineFormset}


class ERPTransactionCreateForm(ERPForm):
    class Meta:
        form_class = TransactionCreateForm
        inlines = {'accounts': TransactionInlineFormset}
