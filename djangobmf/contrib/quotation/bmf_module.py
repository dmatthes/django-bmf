#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.categories import BaseCategory
from djangobmf.categories import Sales
from djangobmf.sites import site

from .models import Quotation
from .views import OpenQuotationView
from .views import AllQuotationView
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


class QuotationCategory(BaseCategory):
    name = _('Quotations')
    slug = "quotations"


site.register_dashboard(Sales)
site.register_category(Sales, QuotationCategory)
site.register_view(Quotation, QuotationCategory, OpenQuotationView)
site.register_view(Quotation, QuotationCategory, AllQuotationView)
