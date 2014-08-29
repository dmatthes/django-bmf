#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

# === VIEWS ===================================================================

from djangobmf.views import ModuleCreateView
from djangobmf.views import ModuleUpdateView
from djangobmf.views import ModuleDetailView

from .forms import DocumentForm


class DocumentCreateView(ModuleCreateView):
    form_class = DocumentForm


class DocumentUpdateView(ModuleUpdateView):
    form_class = DocumentForm


class DocumentDetailView(ModuleDetailView):
    form_class = DocumentForm
