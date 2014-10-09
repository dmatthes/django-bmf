#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.categories import BaseCategory
from djangobmf.categories import Accounting
from djangobmf.sites import site

from .models import Invoice
from .views import OpenInvoiceView
from .views import AllInvoiceView
from .views import InvoiceCreateView
from .views import InvoiceUpdateView
from .views import InvoiceDetailView


site.register(Invoice, **{
    'create': InvoiceCreateView,
    'detail': InvoiceDetailView,
    'update': InvoiceUpdateView,
    'report': True,
})


class InvoiceCategory(BaseCategory):
    name = _('Invoices')
    slug = "invoices"


site.register_dashboard(Accounting)
site.register_category(Accounting, InvoiceCategory)
site.register_view(Invoice, InvoiceCategory, OpenInvoiceView)
site.register_view(Invoice, InvoiceCategory, AllInvoiceView)
