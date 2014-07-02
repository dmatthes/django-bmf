#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.db.models import Sum

from .models import Account


def account_balance(account=None):

    if isinstance(account, Account):
        A = [account]
    elif isinstance(account, int):
        A = Account.objects.filter(pk=account)
    else:
        A = Account.objects.filter(parent=None)

    for item in A:
        debit = item.debits.all().aggregate(Sum('amount'))
        credit = item.credits.all().aggregate(Sum('amount'))

        for child in item.children.all():
            account_balance(child)

#   print item, debit, credit
