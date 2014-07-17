#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.db.models import Sum

from .models import Account


def account_balance(account=None):

    if isinstance(account, Account):
        a = [account]
    elif isinstance(account, int):
        a = Account.objects.filter(pk=account)
    else:
        a = Account.objects.filter(parent=None)

    for item in a:
       #debit = item.debits.all().aggregate(Sum('amount'))
       #credit = item.credits.all().aggregate(Sum('amount'))

        for child in item.children.all():
            account_balance(child)

#   print item, debit, credit
