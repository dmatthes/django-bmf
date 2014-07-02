#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

import django_filters
from django import forms


class HasValueFilter(django_filters.Filter):
    field_class = forms.NullBooleanField

    def filter(self, qs, value):
        if value is not None:
            lookup = '%s__isnull' % self.name
            return qs.exclude(**{lookup: value})
        return qs
