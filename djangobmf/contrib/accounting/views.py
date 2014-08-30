#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from djangobmf.views import ModuleIndexView
from djangobmf.views import ModuleCreateView
from djangobmf.views import ModuleUpdateView
from djangobmf.views import ModuleDetailView

# from .models import Account

from .forms import BMFTransactionUpdateForm
from .forms import BMFTransactionCreateForm


class AccountIndexView(ModuleIndexView):
    pass
#   queryset = Account.objects.all().order_by('tree', 'number', 'name')


class TransactionCreateView(ModuleCreateView):
    form_class = BMFTransactionCreateForm


class TransactionUpdateView(ModuleUpdateView):
    form_class = BMFTransactionUpdateForm


class TransactionDetailView(ModuleDetailView):
    form_class = BMFTransactionUpdateForm
