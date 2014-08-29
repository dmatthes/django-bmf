#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from djangobmf.forms import BMFForm

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


class BMFTransactionUpdateForm(BMFForm):
    class Meta:
        form_class = TransactionUpdateForm
        inlines = {'accounts': TransactionInlineFormset}


class BMFTransactionCreateForm(BMFForm):
    class Meta:
        form_class = TransactionCreateForm
        inlines = {'accounts': TransactionInlineFormset}
