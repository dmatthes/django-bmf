#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from djangoerp.views import PluginCreate
from djangoerp.views import PluginUpdate
from djangoerp.views import PluginDetail

from .forms import ERPInvoiceUpdateForm
from .forms import ERPInvoiceCreateForm


class InvoiceCreateView(PluginCreate):
    form_class = ERPInvoiceCreateForm


class InvoiceUpdateView(PluginUpdate):
    form_class = ERPInvoiceUpdateForm


class InvoiceDetailView(PluginDetail):
    form_class = ERPInvoiceUpdateForm
