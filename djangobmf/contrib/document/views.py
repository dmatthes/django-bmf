#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

# === VIEWS ===================================================================

from djangoerp.views import ModuleCreateView
from djangoerp.views import ModuleUpdateView
from djangoerp.views import ModuleDetailView

from .forms import DocumentForm


class DocumentCreateView(ModuleCreateView):
    form_class = DocumentForm


class DocumentUpdateView(ModuleUpdateView):
    form_class = DocumentForm


class DocumentDetailView(ModuleDetailView):
    form_class = DocumentForm
