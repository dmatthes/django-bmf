#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from djangobmf.views import ModuleCreateView
from djangobmf.views import ModuleUpdateView
from djangobmf.views import ModuleDetailView

from .forms import BMFInvoiceUpdateForm
from .forms import BMFInvoiceCreateForm


class InvoiceCreateView(ModuleCreateView):
    form_class = BMFInvoiceCreateForm


class InvoiceUpdateView(ModuleUpdateView):
    form_class = BMFInvoiceUpdateForm


class InvoiceDetailView(ModuleDetailView):
    form_class = BMFInvoiceUpdateForm
