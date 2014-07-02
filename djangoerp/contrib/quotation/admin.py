#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.contrib import admin
from django.conf import settings

from .models import Quotation, QuotationProduct


class QuotationInline(admin.TabularInline):
    model = QuotationProduct
    extra = 5


class QuotationAdmin(admin.ModelAdmin):
    inlines = [
        QuotationInline,
    ]

admin.site.register(Quotation, QuotationAdmin)
