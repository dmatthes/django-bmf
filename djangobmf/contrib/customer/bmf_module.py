#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangoerp.sites import site

from .models import Customer

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
