#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from djangoerp.categories import SALES
from djangoerp.models import ERPModel
from djangoerp.settings import BASE_MODULE
from djangoerp.fields import CurrencyField
from djangoerp.fields import MoneyField

from djangoerp.contrib.accounting.models import ACCOUNTING_INCOME, ACCOUNTING_EXPENSE

from decimal import Decimal

PRODUCT_SERVICE = 1
PRODUCT_CONSUMABLE = 2
PRODUCT_STOCKABLE = 3
PRODUCT_TYPES = (
    (PRODUCT_SERVICE, _("Service")),
# (PRODUCT_CONSUMABLE,_("Consumable")),
# (PRODUCT_STOCKABLE,_("Stockable")),
)

PRODUCT_NO_BATCH = 1
PRODUCT_NO_SERIAL = 2
PRODUCT_NO = (
    (PRODUCT_NO_BATCH, _("Has batch number")),
    (PRODUCT_NO_SERIAL, _("Has serial number")),
)

# =============================================================================


@python_2_unicode_compatible
class AbstractProduct(ERPModel):
    """
    """
    name = models.CharField(
        _("Name"),
        max_length=255,
        null=False,
        blank=False,
    )
    code = models.CharField(
        _("Product Code"),
        max_length=255,
        null=False,
        blank=True,
        db_index=True,
    )
    type = models.PositiveSmallIntegerField(
        _("Product type"),
        null=False,
        blank=False,
        choices=PRODUCT_TYPES,
        default=PRODUCT_SERVICE,
    )
    can_sold = models.BooleanField(_("Can be sold"), null=False, blank=True, default=False, db_index=True)
    can_purchased = models.BooleanField(_("Can be purchased"), null=False, blank=True, default=False, db_index=True)
    description = models.TextField(_("Description"), null=False, blank=True)
    price = MoneyField(_("Price"), blank=False)
    price_currency = CurrencyField()
    price_precision = models.PositiveSmallIntegerField(default=0, blank=True, null=True, editable=False)
    taxes = models.ManyToManyField(
        BASE_MODULE["TAX"],
        blank=True,
        related_name="product_taxes",
        limit_choices_to={'is_active': True},
        through='ProductTax',
    )
    # discount = models.FloatField(_('Max. discount'), default=0.0)
    # Accounting
    income_account = models.ForeignKey(
        BASE_MODULE["ACCOUNT"],
        null=False,
        blank=False,
        related_name="product_income",
        limit_choices_to={'type': ACCOUNTING_INCOME, 'read_only': False},
        on_delete=models.PROTECT,
    )
    expense_account = models.ForeignKey(
        BASE_MODULE["ACCOUNT"],
        null=False,
        blank=False,
        related_name="product_expense",
        limit_choices_to={'type': ACCOUNTING_EXPENSE, 'read_only': False},
        on_delete=models.PROTECT,
    )
    # warehouse
    # number = models.PositiveSmallIntegerField( _("Product number"), null=True, blank=True, choices=PRODUCT_NO)
    # uos = models.CharField( "UOS", max_length=255, null=False, blank=True, help_text=_("Unit of Service"))
    # uom = models.CharField( "UOM", max_length=255, null=False, blank=True, help_text=_("Unit of Measurement"))
    # customer_taxes
    # supplier_taxes
    # image
    # category
    # warehouse
    # description_web
    # validation method / FIFO or Running average - first in first out
    # aktiv posten
    # garantie
    # end of live
    # netto weight
    # UOM weight
    # supplier
    # cost-center / 
    # pricelist
    # inspection
    # manufactoring
    # online available
    # discount
    # sale_price
    # product_manager
    # warranty: months
    # description_quotation
    # description_suppliers
    # customer_lead_time: days
    # FIFO - First in First out
    # LIFO - Last-in-First-Out
    # sku   Product SKU   required  string  new_product
    # name  Product name  required
    # meta_title  Product meta title  optional  string  new product
    # meta_description
    # price   Product price   required
    # weight  Product weight  required
    # visibility  Product visibility. Can have the following values: 1 - Not Visible Individually, 2 - Catalog, 3 - Search, 4 - Catalog, Search.  required
    # description   Product description.  required
    # short_description   Product short description.  required
    # UOM to UOS
    # Unit weight (Kg)
    # Sales price   0.00
    # Sales currency  EUR
    # Max sales discount (%)  0.00
    # Sales tax (%)   0.00
    # Description   empty
    # Categories  empty
    # Tags  empty

    class Meta(ERPModel.Meta): # only needed for abstract models
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        ordering = ['name']
        abstract = True

    class ERPMeta:
        category = SALES
        search_fields = ['name', 'code']

    def __str__(self):
        return self.name

# def calc_default_price(self, project, amount, price):
#   return self.get_price(1.0, self.price)

    def calc_tax(self, amount, price):
        # TODO add currency for calculation of taxes
        if not isinstance(amount, Decimal):
            amount = Decimal(str(amount))
        if not isinstance(price, Decimal):
            price = Decimal(str(price))

        if price.as_tuple().exponent > -2:
            price = price.quantize(Decimal('0.01'))

        taxes = self.product_tax.select_related('tax')

        tax_inc_sum = Decimal(1)
        for tax in taxes:
            if tax.included:
                tax_inc_sum += tax.tax.get_rate()

        # net price of one unit
        unit_exact = (price / tax_inc_sum).quantize(price)

        used_taxes = []
        net = (amount * unit_exact).quantize(Decimal('0.01'))
        gross = (amount * unit_exact).quantize(Decimal('0.01'))

        for tax in taxes:
            tax_value = (net * tax.tax.get_rate()).quantize(Decimal('0.01'))
            gross += tax_value
            used_taxes.append((tax.tax, tax_value))
        return unit_exact, net, gross, used_taxes


class Product(AbstractProduct):
    pass


class ProductTax(models.Model):
    product = models.ForeignKey(
        BASE_MODULE["PRODUCT"],
        null=True,
        blank=True,
        related_name="product_tax",
        on_delete=models.CASCADE,
    )
    tax = models.ForeignKey(
        BASE_MODULE["TAX"],
        null=True,
        blank=True,
        related_name="product_tax",
        on_delete=models.PROTECT,
    )
    included = models.BooleanField(_("Is the tax included in the price?"), default=False)

    class Meta:
        unique_together = ("product", "tax")
