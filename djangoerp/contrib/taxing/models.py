#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from djangoerp.models import ERPModel
from djangoerp.categories import SETTINGS
from djangoerp.settings import BASE_MODULE

from djangoerp.contrib.accounting.models import ACCOUNTING_LIABILITY

from decimal import Decimal


class AbstractTax(ERPModel):
    name = models.CharField(max_length=255, null=False, blank=False, )
# invoice_name_long = models.CharField( max_length=255, null=False, blank=False, )
# invoice_name_short = models.CharField( max_length=255, null=False, blank=False, )
    account = models.ForeignKey(BASE_MODULE["ACCOUNT"], null=False, blank=False, related_name="tax_liability", limit_choices_to={'type': ACCOUNTING_LIABILITY, 'read_only': False})
    rate = models.DecimalField(max_digits=8, decimal_places=5)
    passive = models.BooleanField(_('Tax is allways included in the product price and never visible to the customer'), null=False, blank=False, default=False)
    is_active = models.BooleanField(_("Is active"), null=False, blank=False, default=True)

    def get_rate(self):
        return self.rate / Decimal(100)

    class Meta:
        verbose_name = _('Tax')
        verbose_name_plural = _('Taxes')
        ordering = ['name']
        abstract = True

    class ERPMeta:
        category = SETTINGS
        observed_fields = ['name', 'invoice_name', 'rate']

    def __unicode__(self):
        return self.name


class Tax(AbstractTax):
    pass
