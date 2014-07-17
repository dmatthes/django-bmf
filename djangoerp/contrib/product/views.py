#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from ...views import ModuleCreateView
from ...views import ModuleUpdateView
from ...views import ModuleDetailView

from .forms import ERPProductUpdateForm
from .forms import ERPProductCreateForm


class ProductCreateView(ModuleCreateView):
    form_class = ERPProductCreateForm


class ProductUpdateView(ModuleUpdateView):
    form_class = ERPProductUpdateForm


class ProductDetailView(ModuleDetailView):
    form_class = ERPProductUpdateForm
