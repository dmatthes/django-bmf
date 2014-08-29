#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from djangobmf.sites import site

from .models import Quotation
from .views import QuotationCreateView
from .views import QuotationDetailView
from .views import QuotationUpdateView
from .views import QuotationTableView

site.register(Quotation, **{
    'index': QuotationTableView,
    'create': QuotationCreateView,
    'detail': QuotationDetailView,
    'update': QuotationUpdateView,
    'report': True,
})
