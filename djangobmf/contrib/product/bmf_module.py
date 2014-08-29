#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django import forms

from djangobmf.sites import site

from .apps import ProductConfig

from .models import Product
from .models import PRODUCT_SERVICE
from .views import ProductCreateView
from .views import ProductDetailView
from .views import ProductUpdateView

site.register(Product, **{
    'create': ProductCreateView,
    'detail': ProductDetailView,
    'update': ProductUpdateView,
})

SETTINGS = {
    'default': forms.ModelChoiceField(queryset=Product.objects.filter(type=PRODUCT_SERVICE)),
}
site.register_settings(ProductConfig.label, SETTINGS)
