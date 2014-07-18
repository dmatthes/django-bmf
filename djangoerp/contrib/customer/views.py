#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from ...views import ModuleCreateView
from ...views import ModuleUpdateView

from .forms import CompanyForm
from .forms import CustomerForm


class BaseCreateView(ModuleCreateView):
    def get_initial(self):
        # TODO: read the configuration here
#       self.initial.update({'asset_account': self.request.erpcore['company'].customer_account_id})
#       self.initial.update({'liability_account': self.request.erpcore['company'].supplier_account_id})
        return super(BaseCreateView, self).get_initial()


class CompanyCreateView(BaseCreateView):
    form_class = CompanyForm

    def form_valid(self, form):
        form.instance.is_company = True
        return super(CompanyCreateView, self).form_valid(form)


class CustomerCreateView(BaseCreateView):
    form_class = CustomerForm


class UpdateView(ModuleUpdateView):
    def get_form_class(self, *args, **kwargs):
        if self.object.is_company:
            return CompanyForm
        return CustomerForm
