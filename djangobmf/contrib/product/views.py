#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from ...views import ModuleCreateView
from ...views import ModuleUpdateView
from ...views import ModuleDetailView

from .forms import BMFProductUpdateForm
from .forms import BMFProductCreateForm


class ProductCreateView(ModuleCreateView):
    form_class = BMFProductCreateForm


class ProductUpdateView(ModuleUpdateView):
    form_class = BMFProductUpdateForm


class ProductDetailView(ModuleDetailView):
    form_class = BMFProductUpdateForm
