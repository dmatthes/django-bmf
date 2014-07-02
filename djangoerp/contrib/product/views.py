#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from djangoerp.views import PluginCreate
from djangoerp.views import PluginUpdate
from djangoerp.views import PluginDetail

from .forms import ERPProductUpdateForm
from .forms import ERPProductCreateForm


class ProductCreateView(PluginCreate):
    form_class = ERPProductCreateForm


class ProductUpdateView(PluginUpdate):
    form_class = ERPProductUpdateForm


class ProductDetailView(PluginDetail):
    form_class = ERPProductUpdateForm
