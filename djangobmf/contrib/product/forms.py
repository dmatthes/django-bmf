#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from djangobmf.forms import BMFForm

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


class BMFProductUpdateForm(BMFForm):
    class Meta:
        form_class = ProductUpdateForm
        inlines = {'taxes': ProductInlineFormset}


class BMFProductCreateForm(BMFForm):
    class Meta:
        form_class = ProductCreateForm
        inlines = {'taxes': ProductInlineFormset}
