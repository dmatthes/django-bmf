#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from djangoerp.forms import ERPForm

from .models import Product
from .models import ProductTax


class ProductUpdateForm(ModelForm):
    class Meta:
        model = Product
        exclude = []


class ProductCreateForm(ModelForm):
    class Meta:
        model = Product
        exclude = []

ProductInlineFormset = inlineformset_factory(Product, ProductTax, extra=1, exclude=[])


class ERPProductUpdateForm(ERPForm):
    class Meta:
        form_class = ProductUpdateForm
        inlines = {'taxes': ProductInlineFormset}


class ERPProductCreateForm(ERPForm):
    class Meta:
        form_class = ProductCreateForm
        inlines = {'taxes': ProductInlineFormset}
