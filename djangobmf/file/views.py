#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.views.generic import CreateView
from django.views.generic import DetailView
from django.http import HttpResponseRedirect
from django.http import Http404
from django.views.static import serve
from django.contrib.contenttypes.models import ContentType
from django.forms.models import modelform_factory

from ..utils import get_model_from_cfg
from ..signals import activity_addfile
from ..viewmixins import BaseMixin


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


class FileDownloadView(BaseMixin, DetailView):
    model = get_model_from_cfg('DOCUMENT')

    def get(self, request, *args, **kwargs):
        # TODO: support static serving via X-Sendfile and generate warnings if not used (and not debug
        self.object = self.get_object()
        return serve(
            request,
            self.object.file.name,
            document_root=self.object.file.storage.base_location,
            show_indexes=False,
        )


class FileAddView(BaseMixin, CreateView):
    """
    table view
    """
    model = get_model_from_cfg('DOCUMENT')
    form_class = modelform_factory(get_model_from_cfg('DOCUMENT'), fields=('file',))

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.get_success_url())

    def get_rel_model(self):
        if hasattr(self, 'related_model'):
            return self.related_model
        try:
            ct = ContentType.objects.get_for_id(self.kwargs['ct'])
        except ContentType.DoesNotExist:
            raise Http404

        self.related_model = ct.model_class()
        if not hasattr(self.related_model, '_bmfmeta'):
            raise Http404

        return self.related_model

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
            activity_addfile.send(
                sender=ct.model_class(),
                instance=ct.model_class().objects.get(pk=pk),
                file=self.object,
            )
        return HttpResponseRedirect(self.get_success_url())

    def get_rel_object(self):
        if hasattr(self, 'related_object'):
            return self.related_object
        try:
            self.related_object = self.get_rel_model().objects.get(pk=self.kwargs['pk'])
        except self.get_rel_model().DoesNotExist:
            raise Http404

        return self.related_object

    def get_success_url(self):
        return self.get_rel_object().bmfmodule_detail()
