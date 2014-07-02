#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from djangoerp.views import PluginCreate
from djangoerp.views import PluginUpdate
from djangoerp.views import PluginDetail

from .forms import ERPTransactionUpdateForm
from .forms import ERPTransactionCreateForm


class TransactionCreateView(PluginCreate):
    form_class = ERPTransactionCreateForm


class TransactionUpdateView(PluginUpdate):
    form_class = ERPTransactionUpdateForm


class TransactionDetailView(PluginDetail):
    form_class = ERPTransactionUpdateForm
