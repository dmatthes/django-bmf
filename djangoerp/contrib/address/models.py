#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from djangoerp.models import ERPModel
from djangoerp.settings import BASE_MODULE
from djangoerp.categories import SALES


class BaseAddress(ERPModel):
    customer = models.ForeignKey(BASE_MODULE["CUSTOMER"], null=False, blank=False, related_name="customer_address")

    is_active = models.BooleanField(_('Is active'), default=True)
    is_billing = models.BooleanField(_('Is billing'),  default=True)
    is_shipping = models.BooleanField(_('Is shipping'),  default=True)
    default_billing = models.BooleanField(_('Default billing'),  default=False)
    default_shipping = models.BooleanField(_('Default shipping'),  default=False)

    def as_report(self):
        raise NotImplementedError('You need to implement a function to print your address in a report')

    class Meta:
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')
        ordering = ['name']
        abstract = True

    class ERPMeta:
        category = SALES

    def erpget_customer(self):
        return self.customer


class AbstractAddress(BaseAddress):
    """
    """
    name = models.CharField(_('Name'),  max_length=255, null=True, blank=False, )
    name2 = models.CharField(_('Name2'),  max_length=255, null=True, blank=True, )
    street = models.CharField(_('Street'),  max_length=255, null=True, blank=False, )
    zip = models.CharField(_('Zipcode'),  max_length=255, null=True, blank=False, )
    city = models.CharField(_('City'),  max_length=255, null=True, blank=False, )
    state = models.CharField(_('State'),  max_length=255, null=True, blank=True, )
    country = models.CharField(_('Country'),  max_length=255, null=True, blank=False, )

    class Meta(BaseAddress.Meta):
        abstract = True

    def as_report(self):
        return _("""
                %(name)s %(name2)s
                %(street)s
                %(city)s, %(state)s, %(zip)s, %(country)s
            """.strip()) % {
                'name': self.name,
                'name2': "\n"+self.name2,
                'street': self.street,
                'zip': self.zip,
                'city': self.city,
                'state': self.state,
                'country': self.country,
                }

    class ERPMeta(BaseAddress.ERPMeta):
        category = SALES
        observed_fields = ['name', 'name2', 'street', 'zip', 'city', 'state', 'country']

    def __unicode__(self):
        if self.name2:
            return self.name+", "+self.name2
        return self.name


class Address(AbstractAddress):
    pass
