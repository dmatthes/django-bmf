#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

import django_filters

from djangobmf.filters import HasValueFilter

from .models import Position


class PositionFilter(django_filters.FilterSet):
    invoice = HasValueFilter()

    class Meta:
        model = Position
        fields = ['project', 'employee', 'product', 'invoice']
        order_by = (
            ('date', '+Date'),
            ('name', '+Name'),
            ('project__name', '+Project'),
            ('product__name', '+Product'),
            ('-date', '-Date'),
            ('-name', '-Name'),
            ('-project__name', '-Project'),
            ('-product__name', '-Product'),
        )
