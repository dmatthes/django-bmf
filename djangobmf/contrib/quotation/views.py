#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from djangoerp.views import ModuleCreateView
from djangoerp.views import ModuleUpdateView
from djangoerp.views import ModuleIndexView
from djangoerp.views import ModuleDetailView

from .forms import ERPQuotationUpdateForm
from .forms import ERPQuotationCreateForm

from .filters import QuotationFilter

import datetime


class QuotationCreateView(ModuleCreateView):
    form_class = ERPQuotationCreateForm

    def get_initial(self):
        self.initial.update({'date': datetime.datetime.now()})
        # LOOK ... this does not work in every case ?!?!
        # self.initial.update({'employee': self.request.djangoerp_employee.pk})
        return super(QuotationCreateView, self).get_initial()


class QuotationUpdateView(ModuleUpdateView):
    form_class = ERPQuotationUpdateForm


class QuotationDetailView(ModuleDetailView):
    form_class = ERPQuotationUpdateForm


class QuotationTableView(ModuleIndexView):
    filterset_class = QuotationFilter
