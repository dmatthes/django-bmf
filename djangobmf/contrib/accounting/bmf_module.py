#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _

from djangobmf.categories import BaseCategory
from djangobmf.categories import Accounting
from djangobmf.sites import site

from collections import OrderedDict

from .apps import AccountingConfig

from .models import ACCOUNTING_INCOME
from .models import ACCOUNTING_EXPENSE
from .models import ACCOUNTING_ASSET
from .models import ACCOUNTING_LIABILITY

from .models import Account
from .views import AccountIndexView


site.register(Account, **{
    'index': AccountIndexView,
})


from .models import Transaction
from .views import OpenTransactionView
from .views import TransferView
from .views import TransactionCreateView
from .views import TransactionDetailView
from .views import TransactionUpdateView

site.register(Transaction, **{
    'create': OrderedDict((
        ('transfer', (_('Between two Accounts'), TransferView)),
        ('template', (_('Split Transaction'), TransactionCreateView)),
    )),
    'detail': TransactionDetailView,
    'update': TransactionUpdateView,
})

from .models import TransactionItem
from .views import AllTransactionView


site.register(TransactionItem)


SETTINGS = {
    'income': forms.ModelChoiceField(queryset=Account.objects.filter(type=ACCOUNTING_INCOME)),
    'expense': forms.ModelChoiceField(queryset=Account.objects.filter(type=ACCOUNTING_EXPENSE)),
    'customer': forms.ModelChoiceField(queryset=Account.objects.filter(type=ACCOUNTING_ASSET)),
    'supplier': forms.ModelChoiceField(queryset=Account.objects.filter(type=ACCOUNTING_LIABILITY)),
}
site.register_settings(AccountingConfig.label, SETTINGS)


class TransactionCategory(BaseCategory):
    name = _('Transactions')
    slug = "transactions"


site.register_dashboard(Accounting)

site.register_category(Accounting, TransactionCategory)
site.register_view(Account, TransactionCategory, AccountIndexView)
site.register_view(Transaction, TransactionCategory, OpenTransactionView)
site.register_view(TransactionItem, TransactionCategory, AllTransactionView)
