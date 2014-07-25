#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.contrib import admin

from .models import Transaction, TransactionItem


class TransactionInline(admin.TabularInline):
    model = TransactionItem
    extra = 2


class TransactionAdmin(admin.ModelAdmin):
    inlines = [
        TransactionInline,
    ]

admin.site.register(Transaction, TransactionAdmin)
