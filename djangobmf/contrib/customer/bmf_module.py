#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.categories import BaseCategory
from djangobmf.categories import Sales
from djangobmf.sites import site

from .models import Customer

from .views import AllCustomerView
from .views import CustomerCustomerView
from .views import SupplierCustomerView
from .views import CustomerCreateView
from .views import CompanyCreateView
from .views import UpdateView

site.register(Customer, **{
    'create': {
        u'company': (_('Company'), CompanyCreateView),
        u'customer': (_('Customer'), CustomerCreateView),
    },
    'update': UpdateView,
})


class CustomerCategory(BaseCategory):
    name = _('Customer')
    slug = "customer"


site.register_dashboard(Sales)
site.register_category(Sales, CustomerCategory)
site.register_view(Customer, CustomerCategory, AllCustomerView)
site.register_view(Customer, CustomerCategory, CustomerCustomerView)
site.register_view(Customer, CustomerCategory, SupplierCustomerView)
