#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
# from django.forms.models import modelform_factory
from django.http import HttpResponseRedirect
from django.http import Http404
from django.utils.timezone import now
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.static import serve

from djangobmf.signals import activity_addfile
from djangobmf.viewmixins import BaseMixin

from .forms import UploadDocument
from .models import Document

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

  sendtype = getattr(settings,"BMF_DOCUMENTS_SEND",None)

  if sendtype == "accelredirect" and not settings.DEBUG:
    response = HttpResponse()
    response['Content-Type'] = ''
    response['X-Accel-Redirect'] = fileobject.url # TODO not tested if this works with apache
    return response

  if sendtype == "sendfile" and not settings.DEBUG:
    response = HttpResponse()
    response['Content-Type'] = ''
    response['X-Sendfile'] = (os.path.join(settings.BMF_DOCUMENTS_ROOT, fileobject.url)).encode('utf-8')
    return response

  # serve with django
  return serve(request,fileobject.url[len(settings.BMF_DOCUMENTS_URL):],document_root=settings.BMF_DOCUMENTS_ROOT)
'''


class DocumentDownloadView(BaseMixin, DetailView):
    model = Document

    def get(self, request, *args, **kwargs):
        # TODO: support static serving via X-Sendfile and generate warnings if not used (and not debug
        self.object = self.get_object()
        return serve(
            request,
            self.object.file.name,
            document_root=self.object.file.storage.base_location,
            show_indexes=False,
        )


class DocumentCreateView(BaseMixin, CreateView):
    model = Document
    form_class = UploadDocument

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.get_success_url())

    def post(self, request, *args, **kwargs):
        return super(DocumentCreateView, self).post(request, *args, **kwargs)

    def form_invalid(self, form):
        return HttpResponseRedirect(self.get_success_url())

    def form_valid(self, form):
        if form.instance.file:
            ct = ContentType.objects.get_for_id(self.kwargs['ct'])
            pk = int(self.kwargs['pk'])
            form.instance.created_by = self.request.user
            form.instance.modified_by = self.request.user
            form.instance.content_type = ct
            form.instance.content_id = pk
            self.object = form.save()

            content_object = ct.model_class().objects.get(pk=pk)
            content_object.modified = now()
            content_object.modified_by = self.request.user
            content_object.save()

            activity_addfile.send(
                sender=ct.model_class(),
                instance=content_object,
                file=self.object,
            )
        return HttpResponseRedirect(self.get_success_url())

    def get_rel_object(self):
        if hasattr(self, 'related_object'):
            return self.related_object

        try:
            ct = ContentType.objects.get_for_id(self.kwargs['ct'])
            model = ct.model_class()

            self.related_object = model.objects.get(pk=self.kwargs['pk'])

        except model.DoesNotExist:
            raise Http404

        return self.related_object

    def get_success_url(self):
        return self.get_rel_object().bmfmodule_detail()
