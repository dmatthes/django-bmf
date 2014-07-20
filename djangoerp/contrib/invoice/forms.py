#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.forms import ModelForm

from django.forms.models import inlineformset_factory

from djangoerp.forms import ERPForm

from .models import Invoice, InvoiceProduct


class InvoiceUpdateForm(ModelForm):
    class Meta:
        model = Invoice
        exclude = ['invoice_number', ]


class InvoiceCreateForm(ModelForm):
    class Meta:
        model = Invoice
        exclude = ['invoice_number', 'state', 'shipping_address', 'invoice_address', 'valid_until']


InvoiceInlineFormset = inlineformset_factory(Invoice, InvoiceProduct, extra=2, exclude=[])


class ERPInvoiceUpdateForm(ERPForm):
    class Meta:
        form_class = InvoiceUpdateForm
        inlines = {'products': InvoiceInlineFormset}


class ERPInvoiceCreateForm(ERPForm):
    class Meta:
        form_class = InvoiceCreateForm
        inlines = {'products': InvoiceInlineFormset}
