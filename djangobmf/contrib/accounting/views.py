#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.views import ModuleGenericListView
from djangobmf.views import ModuleCreateView
from djangobmf.views import ModuleUpdateView
from djangobmf.views import ModuleDetailView

# from .models import Account

from .forms import BMFTransactionUpdateForm
from .forms import BMFTransactionCreateForm


class AccountIndexView(ModuleGenericListView):
    name = _("All Accounts")
    slug = "all"


class TransactionCreateView(ModuleCreateView):
    form_class = BMFTransactionCreateForm


class TransactionUpdateView(ModuleUpdateView):
    form_class = BMFTransactionUpdateForm


class TransactionDetailView(ModuleDetailView):
    form_class = BMFTransactionUpdateForm
