#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django import forms

from djangobmf.sites import site

from .apps import AccountingConfig

from .models import ACCOUNTING_INCOME
from .models import ACCOUNTING_EXPENSE
from .models import ACCOUNTING_ASSET
from .models import ACCOUNTING_LIABILITY

from .models import Account
site.register(Account)

from .models import Transaction
from .views import TransactionCreateView
from .views import TransactionDetailView
from .views import TransactionUpdateView

site.register(Transaction, **{
    'create': TransactionCreateView,
    'detail': TransactionDetailView,
    'update': TransactionUpdateView,
})

SETTINGS = {
    'income': forms.ModelChoiceField(queryset=Account.objects.filter(type=ACCOUNTING_INCOME)),
    'expense': forms.ModelChoiceField(queryset=Account.objects.filter(type=ACCOUNTING_EXPENSE)),
    'customer': forms.ModelChoiceField(queryset=Account.objects.filter(type=ACCOUNTING_ASSET)),
    'supplier': forms.ModelChoiceField(queryset=Account.objects.filter(type=ACCOUNTING_LIABILITY)),
}
site.register_settings(AccountingConfig.label, SETTINGS)
