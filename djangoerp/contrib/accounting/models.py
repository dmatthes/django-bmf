#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

"""
models doctype
"""

from django.db import models
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _

from djangoerp.models import ERPMPTTModel
from djangoerp.models import ERPModel
from djangoerp.categories import ACCOUNTING
from djangoerp.settings import BASE_MODULE
from djangoerp.fields import CurrencyField
from djangoerp.fields import MoneyField
from djangoerp.fields import WorkflowField

from .workflows import TransactionWorkflow

from decimal import Decimal
from mptt.models import TreeForeignKey

ACCOUNTING_INCOME = 10
ACCOUNTING_EXPENSE = 20
ACCOUNTING_ASSET = 30
ACCOUNTING_LIABILITY = 40
ACCOUNTING_EQUITY = 50

ACCOUNTING_TYPES = (
    (ACCOUNTING_INCOME, _('Income')),
    (ACCOUNTING_EXPENSE, _('Expense')),
    (ACCOUNTING_ASSET, _('Asset')),
    (ACCOUNTING_LIABILITY, _('Liability')),
    (ACCOUNTING_EQUITY, _('Equity')),
)

# =============================================================================

# TODO: Add Fiscal Year
# TODO: Add Period

# =============================================================================


class BaseAccount(ERPMPTTModel):
    """
    """
    parent = TreeForeignKey(
        'self', null=True, blank=True, related_name='children',
        on_delete=models.CASCADE,
    )
#   parent = models.ForeignKey('self', null=True, blank=True, related_name='children')
    balance = MoneyField(editable=False, default="0")
    balance_currency = CurrencyField()
    number = models.CharField(_('Number'), max_length=30, null=True, blank=True, )
    name = models.CharField(_('Name'), max_length=100, null=False, blank=False, )
    type = models.PositiveSmallIntegerField(
        _('Type'), null=False, blank=False, choices=ACCOUNTING_TYPES,
    )
    read_only = models.BooleanField(_('Read-only'), default=False)

    def get_balance(self):
        # items = list(self.get_descendants().values_list('pk', flat=True))
        # items.append(self.pk)
        # bal_credit = self.transaction_accounts.model.objects.filter(pk__in=items, balanced=True, credit=True).aggregate(Sum('amount'))
        # bal_debit = self.transaction_accounts.model.objects.filter(pk__in=items, balanced=True, credit=False).aggregate(Sum('amount'))
        bal_credit = self.transaction_accounts.filter(
            balanced=True,
            credit=True,
        ).aggregate(Sum('amount'))
        bal_debit = self.transaction_accounts.filter(
            balanced=True,
            credit=False,
        ).aggregate(Sum('amount'))
        number_credit = bal_credit['amount__sum'] or Decimal(0)
        number_debit = bal_debit['amount__sum'] or Decimal(0)
        if self.type in [ACCOUNTING_ASSET, ACCOUNTING_EXPENSE]:
            return (number_debit - number_credit).quantize(Decimal('0.01'))
        else:
            return (number_credit - number_debit).quantize(Decimal('0.01'))

    class Meta:
        verbose_name = _('Account')
        verbose_name_plural = _('Accounts')
        ordering = ['number', 'name', 'type']
        abstract = True

    class ERPMeta:
        category = ACCOUNTING
        observed_fields = ['name', ]

    def __unicode__(self):
        return '%s: %s' % (self.number, self.name)


class AbstractAccount(BaseAccount):
    """
    """
    comment = models.TextField(_('Comment'), blank=True, null=True)

    class Meta(BaseAccount.Meta):
        abstract = True

    class ERPMeta(BaseAccount.ERPMeta):
        search_fields = ['name', 'number']


class Account(AbstractAccount):
    """
    """
    pass

# =============================================================================


class AbstractTransaction(ERPModel):
    """
    Transaction

    ==============  ========  ========
    Account-Type     Credit     Debit
    ==============  ========  ========
    Asset           Decrease  Increase
    Liability       Increase  Decrease
    Income/Revenue  Increase  Decrease
    Expense         Decrease  Increase
    Equity/Capital  Increase  Decrease
    ==============  ========  ========
    """
    state = WorkflowField()
    if BASE_MODULE["PROJECT"]:
        project = models.ForeignKey(
            BASE_MODULE["PROJECT"], null=True, blank=True, on_delete=models.SET_NULL,
        )
    text = models.CharField(
        _('Posting text'), max_length=255, null=False, blank=False,
    )
    accounts = models.ManyToManyField(BASE_MODULE["ACCOUNT"], blank=False, through="TransactionItem")
    balanced = models.BooleanField(_('Draft'), default=False, editable=False)

# expensed = models.BooleanField(_('Expensed'), blank=True, null=False, default=False, )

    class Meta:
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')
        abstract = True

    class ERPMeta:
        category = ACCOUNTING
        observed_fields = ['expensed', 'text']
        has_files = True
        workflow = TransactionWorkflow
        workflow_field = 'state'

    def __unicode__(self):
        return '%s' % self.text


class Transaction(AbstractTransaction):
    """
    """
    pass


class TransactionItemManager(models.Manager):
    """
    """
    def get_queryset(self):
        return super(TransactionItemManager, self).get_queryset().select_related('account').extra(select={"type": "type"})


class AbstractTransactionItem(models.Model):
    """
    """
    account = models.ForeignKey(
        BASE_MODULE["ACCOUNT"], null=True, blank=True,
        related_name="transaction_accounts", on_delete=models.PROTECT,
    )
    transaction = models.ForeignKey(
        BASE_MODULE["TRANSACTION"], null=True, blank=True,
        related_name="account_transactions", on_delete=models.CASCADE,
    )
    amount = MoneyField()
    amount_currency = CurrencyField()
    credit = models.BooleanField(
        choices=((True, _('Credit')), (False, _('Debit'))),
        default=True,
    )
    balanced = models.BooleanField(default=False, editable=False)
    modified = models.DateTimeField(
        _("Modified"), auto_now=True, editable=False, null=True, blank=False,
    )

    objects = TransactionItemManager()

    class Meta:
        abstract = True

# def set_debit(self, amount):
#   if self.get_type in [ACCOUNTING_ASSET, ACCOUNTING_EXPENSE]:
#     self.amount =  amount
#   else:
#     self.amount = -amount

# def set_credit(self, amount):
#   if self.get_type in [ACCOUNTING_ASSET, ACCOUNTING_EXPENSE]:
#     self.amount = -amount
#   else:
#     self.amount =  amount

    @property
    def get_type(self):
        try:
            return getattr(self, 'type', self.account.type)
        except AttributeError:
            return 0

# @property
# def is_debit(self):
#   if self.type in [ACCOUNTING_ASSET, ACCOUNTING_EXPENSE]:
#     return self.amount > 0.
#   else:
#     return self.amount < 0.

# @property
# def is_credit(self):
#   return not self.is_debit

# @property
# def get_transation(self):
#   if self.is_debit:
#     return (abs(self.amount), 0)
#   else:
#     return (0, abs(self.amount))


class TransactionItem(AbstractTransactionItem):
    """
    This only inherits from AbstractTransactionItem.
    """
    pass
