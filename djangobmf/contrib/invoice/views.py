#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from djangoerp.views import ModuleCreateView
from djangoerp.views import ModuleUpdateView
from djangoerp.views import ModuleDetailView

from .forms import ERPInvoiceUpdateForm
from .forms import ERPInvoiceCreateForm


class InvoiceCreateView(ModuleCreateView):
    form_class = ERPInvoiceCreateForm


class InvoiceUpdateView(ModuleUpdateView):
    form_class = ERPInvoiceUpdateForm


class InvoiceDetailView(ModuleDetailView):
    form_class = ERPInvoiceUpdateForm
