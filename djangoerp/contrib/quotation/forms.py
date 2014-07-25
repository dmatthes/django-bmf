#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.forms import ModelForm

from django.forms.models import inlineformset_factory

from djangoerp.forms import ERPForm
# rom djangoerp.layouts import Helper, Layout

from .models import Quotation, QuotationProduct


class QuotationUpdateForm(ModelForm):
    class Meta:
        model = Quotation
        exclude = ['quotation_number', ]


class QuotationCreateForm(ModelForm):
    class Meta:
        model = Quotation
        exclude = ['quotation_number', 'state', 'shipping_address', 'invoice_address', 'valid_until']


QuotationInlineFormset = inlineformset_factory(Quotation, QuotationProduct, extra=2, exclude=[])


class ERPQuotationUpdateForm(ERPForm):
    class Meta:
        form_class = QuotationUpdateForm
        inlines = {'products': QuotationInlineFormset}


class ERPQuotationCreateForm(ERPForm):
    class Meta:
        form_class = QuotationCreateForm
        inlines = {'products': QuotationInlineFormset}
