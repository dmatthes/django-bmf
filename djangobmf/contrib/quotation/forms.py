#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.forms import ModelForm

from django.forms.models import inlineformset_factory

from djangobmf.forms import BMFForm
# rom djangobmf.layouts import Helper, Layout

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


class BMFQuotationUpdateForm(BMFForm):
    class Meta:
        form_class = QuotationUpdateForm
        inlines = {'products': QuotationInlineFormset}


class BMFQuotationCreateForm(BMFForm):
    class Meta:
        form_class = QuotationCreateForm
        inlines = {'products': QuotationInlineFormset}
