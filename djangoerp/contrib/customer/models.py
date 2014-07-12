#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from djangoerp.models import ERPModel
from djangoerp.categories import SALES
from djangoerp.settings import BASE_MODULE
from djangoerp.utils import get_model_from_name

from djangoerp.contrib.accounting.models import ACCOUNTING_ASSET, ACCOUNTING_LIABILITY


class BaseCustomer(ERPModel):
    name = models.CharField(_("Name"), max_length=255, null=True, blank=False, )
    number = models.CharField(_("Number"), max_length=255, null=True, blank=True, )
    user = models.ForeignKey(getattr(settings, 'AUTH_USER_MODEL', 'auth.User'), blank=True, null=True, related_name="erp_customer", on_delete=models.SET_NULL)

    if BASE_MODULE["PROJECT"]:
        project = models.ForeignKey(BASE_MODULE["PROJECT"], null=True, blank=True, related_name="+", on_delete=models.SET_NULL,
            help_text=_("Projects function as cost-centers. This setting defines a default project for this customer.")) # TODO edit queryset for projects (show only company projects and own ones)

    employee_at = models.ForeignKey('self', null=True, blank=True, limit_choices_to={'is_company': True}, on_delete=models.SET_NULL)
    is_company = models.BooleanField(_("Is Company"), default=False)

    taxvat = models.CharField(_("Taxvat"), max_length=255, null=True, blank=True, )

    use_company_addresses = models.BooleanField(_("Can use company adresses"), default=True)

    is_active = models.BooleanField(_("Is active"), default=True)
    is_customer = models.BooleanField(_("Is customer"), default=True)
    is_supplier = models.BooleanField(_("Is supplier"), default=False)

# TODO add language
# TODO add timezone

    if BASE_MODULE["ACCOUNT"]:
        asset_account = models.ForeignKey(BASE_MODULE["ACCOUNT"], null=True, blank=False, related_name="customer_asset", limit_choices_to={'type': ACCOUNTING_ASSET, 'read_only': False}, on_delete=models.PROTECT)
        liability_account = models.ForeignKey(BASE_MODULE["ACCOUNT"], null=True, blank=False, related_name="customer_liability", limit_choices_to={'type': ACCOUNTING_LIABILITY, 'read_only': False}, on_delete=models.PROTECT)
    customer_payment_term = models.PositiveSmallIntegerField(editable=False, default=1)
    supplier_payment_term = models.PositiveSmallIntegerField(editable=False, default=1)


    class Meta:
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')
        ordering = ['name']
        abstract = True

    class ERPMeta:
        category = SALES
        search_fields = ['name', ]
        has_logging = True
        has_comments = True
        has_files = True

    def __init__(self, *args, **kwargs):
        super(BaseCustomer, self).__init__(*args, **kwargs)
        self.pre_name = self.name
        self.pre_active = self.is_active

    def erpget_customer(self):
        return self

    @staticmethod
    def post_save(sender, instance, created, raw, *args, **kwargs):
        Project = get_model_from_name(BASE_MODULE['PROJECT'])
        if created:
            # create project
            p = Project(name=instance.name, customer=instance, is_bound=True)
            p.save()

        elif instance.pre_name != instance.name or instance.pre_active != instance.is_active or not instance.project:
            # update project
            p, c = Project.objects.get_or_create(customer=instance, is_bound=True)
            p.name = instance.name
            p.is_active = instance.is_active
            p.save()

        if not instance.project:
            instance.project = p
            instance.save()


@python_2_unicode_compatible
class AbstractCustomer(BaseCustomer):
   #image = models.ImageField(null=True, blank=True, upload_to="test") # FIXME
    name2 = models.CharField(_("Name 2"), max_length=255, null=True, blank=True, )
    job_position = models.CharField(_("Job position"), max_length=255, null=True, blank=True, )
    title = models.CharField(_("Title"), max_length=255, null=True, blank=True, )
    phone_office = models.CharField(_("Phone office"), max_length=255, null=True, blank=True, )
    phone_privat = models.CharField(_("Phone privat"), max_length=255, null=True, blank=True, )
    phone_mobile = models.CharField(_("Phone mobile"), max_length=255, null=True, blank=True, )
    email = models.EmailField(_("Email"), null=True, blank=True)
    fax = models.CharField(_("Fax"), max_length=255, null=True, blank=True, )
    website = models.URLField(_("Website"), null=True, blank=True, )
    notes = models.TextField(_("Notes"), null=True, blank=True, )

    class Meta(BaseCustomer.Meta):
        abstract = True

    class ERPMeta(BaseCustomer.ERPMeta):
        observed_fields = ['name', 'email', 'taxvat']
        search_fields = BaseCustomer.ERPMeta.search_fields + ['number', 'email', 'user__username']

    def __str__(self):
        return self.name


class Customer(AbstractCustomer):
    pass
