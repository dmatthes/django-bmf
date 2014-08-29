#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from djangoerp.sites import site

from .models import Document
from .views import DocumentDetailView
from .views import DocumentUpdateView
from .views import DocumentCreateView

site.register(Document, **{
    'create': DocumentCreateView,
    'update': DocumentUpdateView,
    'detail': DocumentDetailView,
})
