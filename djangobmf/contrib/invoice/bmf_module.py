#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from djangoerp.sites import site

from .models import Invoice
from .views import InvoiceCreateView
from .views import InvoiceUpdateView
from .views import InvoiceDetailView

site.register(Invoice, **{
    'create': InvoiceCreateView,
    'detail': InvoiceDetailView,
    'update': InvoiceUpdateView,
    'report': True,
})
