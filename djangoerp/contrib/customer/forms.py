#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from .models import Customer


class CompanyForm(ModelForm):
    class Meta:
        model = Customer
        exclude = ['user', 'employee_at', 'is_company', 'use_company_addresses', 'job_position', 'title', 'phone_mobile', 'phone_privat']


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        exclude = ['is_company']
