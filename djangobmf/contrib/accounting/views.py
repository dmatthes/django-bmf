#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.views import ModuleArchiveView
from djangobmf.views import ModuleListView
from djangobmf.views import ModuleTreeView
from djangobmf.views import ModuleCreateView
from djangobmf.views import ModuleUpdateView
from djangobmf.views import ModuleDetailView

# from .models import Account

from .forms import BMFTransactionUpdateForm
from .forms import BMFTransactionCreateForm


class AccountIndexView(ModuleListView):
    name = _("All Accounts")
    slug = "accounts"


class AllTransactionView(ModuleArchiveView):
    name = _("All Transactions")
    slug = "transactions"


class OpenTransactionView(ModuleTreeView):
    name = _("Open Transactions")
    slug = "items"


class TransferView(ModuleCreateView):
    form_class = BMFTransactionCreateForm


class TransactionCreateView(ModuleCreateView):
    form_class = BMFTransactionCreateForm


class TransactionUpdateView(ModuleUpdateView):
    form_class = BMFTransactionUpdateForm


class TransactionDetailView(ModuleDetailView):
    form_class = BMFTransactionUpdateForm
