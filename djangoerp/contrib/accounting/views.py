#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from djangoerp.views import ModuleCreateView
from djangoerp.views import ModuleUpdateView
from djangoerp.views import ModuleDetailView

from .forms import ERPTransactionUpdateForm
from .forms import ERPTransactionCreateForm


class TransactionCreateView(ModuleCreateView):
    form_class = ERPTransactionCreateForm


class TransactionUpdateView(ModuleUpdateView):
    form_class = ERPTransactionUpdateForm


class TransactionDetailView(ModuleDetailView):
    form_class = ERPTransactionUpdateForm
