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

'''

from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden, Http404
from django.views.static import serve

import os

def sendfile(request, fileobject, allowed=True):
  if not allowed and not request.user.is_superuser:
    return HttpResponseForbidden()

  if not fileobject:
    return Http404

  sendtype = getattr(settings,"ERP_DOCUMENTS_SEND",None)
  if sendtype == "accelredirect" and not settings.DEBUG:
    response = HttpResponse()
    response['Content-Type'] = ''
    response['X-Accel-Redirect'] = fileobject.url # TODO not tested if this works with apache
    return response

  if sendtype == "sendfile" and not settings.DEBUG:
    response = HttpResponse()
    response['Content-Type'] = ''
    response['X-Sendfile'] = (os.path.join(settings.ERP_DOCUMENTS_ROOT, fileobject.url)).encode('utf-8')
    return response

  # serve with django
  return serve(request,fileobject.url[len(settings.ERP_DOCUMENTS_URL):],document_root=settings.ERP_DOCUMENTS_ROOT)

'''
