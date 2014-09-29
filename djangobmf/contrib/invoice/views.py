#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.views import ModuleArchiveView
from djangobmf.views import ModuleListView
from djangobmf.views import ModuleCreateView
from djangobmf.views import ModuleUpdateView
from djangobmf.views import ModuleDetailView

from .forms import BMFInvoiceUpdateForm
from .forms import BMFInvoiceCreateForm


class AllInvoiceView(ModuleArchiveView):
    name = _("All Invoices")
    slug = "all"
    date_resolution = "month"


class OpenInvoiceView(ModuleListView):
    name = _("Open Invoices")
    slug = "open"


class InvoiceCreateView(ModuleCreateView):
    form_class = BMFInvoiceCreateForm


class InvoiceUpdateView(ModuleUpdateView):
    form_class = BMFInvoiceUpdateForm


class InvoiceDetailView(ModuleDetailView):
    form_class = BMFInvoiceUpdateForm
