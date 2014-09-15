#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from djangobmf.models import BMFModel
from djangobmf.categories import ACCOUNTING
from djangobmf.settings import CONTRIB_CUSTOMER
from djangobmf.settings import CONTRIB_PRODUCT
from djangobmf.settings import CONTRIB_PROJECT
from djangobmf.settings import CONTRIB_EMPLOYEE
from djangobmf.settings import CONTRIB_INVOICE
from djangobmf.settings import CONTRIB_ADDRESS
from djangobmf.settings import CONTRIB_TRANSACTION
from djangobmf.fields import WorkflowField
from djangobmf.numbering.utils import numbercycle_get_name, numbercycle_delete_object
from djangobmf.fields import CurrencyField
from djangobmf.fields import MoneyField

import datetime
from decimal import Decimal

from .workflows import InvoiceWorkflow


@python_2_unicode_compatible
class BaseInvoice(BMFModel):

    state = WorkflowField()
    shipping_address = models.ForeignKey(
        CONTRIB_ADDRESS, related_name="shipping_invoice",
        blank=False, null=True, on_delete=models.SET_NULL,
    )
    invoice_address = models.ForeignKey(
        CONTRIB_ADDRESS, related_name="quotation_invoice", blank=False,
        null=True, on_delete=models.SET_NULL,
    )
    invoice_number = models.CharField(_('Invoice number'), max_length=255, null=True, blank=False)
    products = models.ManyToManyField(CONTRIB_PRODUCT, through='InvoiceProduct')
    net = models.FloatField(editable=False, blank=True, null=True)
    date = models.DateField(_("Date"), null=True, blank=False)

    transaction = models.ForeignKey(
        CONTRIB_TRANSACTION, null=True, blank=True, related_name="transation_invoice",
        editable=False, on_delete=models.PROTECT,
    )

    @staticmethod
    def post_save(sender, instance, created, raw, *args, **kwargs):
        if not instance.invoice_number:
            name = numbercycle_get_name(instance)
            instance._meta.model.objects.filter(pk=instance.pk).update(invoice_number=name)

    def __str__(self):
        return '%s' % self.invoice_number

    class BMFMeta:
        category = ACCOUNTING
        number_cycle = "INV{year}/{month}-{counter:04d}"
        workflow = InvoiceWorkflow
        workflow_field = 'state'

    class Meta:
        verbose_name = _('Invoice')
        verbose_name_plural = _('Invoices')
        ordering = ['invoice_number']
        abstract = True
        swappable = "BMF_CONTRIB_INVOICE"


class AbstractInvoice(BaseInvoice):
    """
    """
    customer = models.ForeignKey(  # TODO: make optional
        CONTRIB_CUSTOMER,
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
    )
    project = models.ForeignKey(  # TODO: make optional
        CONTRIB_PROJECT, null=True, blank=False, on_delete=models.SET_NULL,
    )
    employee = models.ForeignKey(  # TODO: make optional
        CONTRIB_EMPLOYEE, null=True, blank=False, on_delete=models.SET_NULL,
    )

    due = models.DateField(_("Due"), null=True, blank=True)
    notes = models.TextField(_("Notes"), null=True, blank=True)
    term_of_payment = models.TextField(_("Term of payment"), blank=True, null=True)

    class Meta(BaseInvoice.Meta):
        abstract = True

    class BMFMeta(BaseInvoice.BMFMeta):
        has_files = True
        has_comments = True

    def bmfget_customer(self):
        if hasattr(self, 'customer'):
            return self.customer
        return None

    def bmfget_project(self):
        if hasattr(self, 'project'):
            return self.project
        return None

    @staticmethod
    def post_delete(sender, instance, *args, **kwargs):
        numbercycle_delete_object(instance)

    def get_products(self):
        if not hasattr(self, '_cache_products'):
            self._cache_products = self.invoice_products.all().select_related('product')
        return self._cache_products

    def calc_net(self):
        val = Decimal(0)
        for item in self.get_products():
            val += item.calc_net()
        return val

    def calc_gross(self):
        val = Decimal(0)
        for item in self.get_products():
            val += item.calc_gross()
        return val

    def calc_taxes(self):
        t = {}
        for item in self.get_products():
            for tax, value in item.calc_taxes():
                if tax in t:
                    t[tax] += value
                else:
                    t[tax] = value
        return t.items()

    def clean(self):
        # if self.project and not self.customer_id:
        #     self.customer = self.project.customer
        # if self.project and not self.employee_id:
        #     self.employee_id = self.project.employee_id
        # if self.customer and not self.project_id:
        #     self.project = self.customer.project
        if self.customer and not self.invoice_address_id:
            self.invoice_address = \
                self.customer.customer_address.filter(is_billing=True, default_billing=True).first()
        if self.customer and not self.shipping_address_id:
            self.shipping_address = \
                self.customer.customer_address.filter(is_shipping=True, default_shipping=True).first()

        if not self.date:
            self.date = datetime.datetime.now().date()


class Invoice(AbstractInvoice):
    pass


class InvoiceProduct(models.Model):
    invoice = models.ForeignKey(
        CONTRIB_INVOICE, null=True, blank=True,
        related_name="invoice_products", on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        CONTRIB_PRODUCT, null=True, blank=True,
        related_name="invoice_products", on_delete=models.PROTECT,
    )
    name = models.CharField(_("Name"), max_length=255, null=True, blank=False)
    price_currency = CurrencyField()
    price_precision = models.PositiveSmallIntegerField(
        default=0, blank=True, null=True, editable=False,
    )
    price = MoneyField(_("Price"), blank=False)
    amount = models.FloatField(_("Amount"), null=True, blank=False, default=1.0)
    # unit = models.CharField() # TODO add units
    description = models.TextField(_("Description"), null=True, blank=True)

    def __init__(self, *args, **kwargs):
        super(InvoiceProduct, self).__init__(*args, **kwargs)
        self._calcs = None

    def clean(self):
        if self.product and not self.name:
            self.name = self.product.name
        if self.product and not self.price:
            self.price = self.product.price

    def calc_all(self):
        if self._calcs:
            return self._calcs
        self._calcs = self.product.calc_tax(self.amount, self.price)
        return self._calcs

    def calc_net_unit(self):
        return self.calc_all()[0]

    def calc_net(self):
        return self.calc_all()[1]

    def calc_gross(self):
        return self.calc_all()[2]

    def calc_taxes(self):
        return self.calc_all()[3]
