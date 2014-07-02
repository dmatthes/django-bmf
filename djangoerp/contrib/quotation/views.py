#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from djangoerp.views import PluginCreate
from djangoerp.views import PluginUpdate
from djangoerp.views import PluginIndex
from djangoerp.views import PluginDetail

from .forms import ERPQuotationUpdateForm
from .forms import ERPQuotationCreateForm

from .filters import QuotationFilter

import datetime


class QuotationCreateView(PluginCreate):
    form_class = ERPQuotationCreateForm

    def get_initial(self):
        self.initial.update({'date': datetime.datetime.now()})
        # LOOK ... this does not work in every case ?!?!
#       self.initial.update({'employee': self.request.djangoerp_employee.pk})
        return super(QuotationCreateView, self).get_initial()


class QuotationUpdateView(PluginUpdate):
    form_class = ERPQuotationUpdateForm


class QuotationDetailView(PluginDetail):
    form_class = ERPQuotationUpdateForm


class QuotationTableView(PluginIndex):
    filterset_class = QuotationFilter
