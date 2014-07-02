#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

import django_filters

from .models import Quotation
from .workflows import QuotationWorkflow


class QuotationFilter(django_filters.FilterSet):
    state = django_filters.MultipleChoiceFilter(choices=QuotationWorkflow()._states.items())

    class Meta:
        model = Quotation
        fields = ['state']
