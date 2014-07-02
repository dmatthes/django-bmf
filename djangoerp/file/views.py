#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.decorators import method_decorator
from django.views.generic import CreateView
from django.http import HttpResponseRedirect
from django.http import Http404
from django.views.defaults import permission_denied
from django.contrib.contenttypes.models import ContentType
from django.forms.models import modelform_factory

from ..utils import get_model_from_cfg
from ..decorators import login_required
from ..signals import activity_addfile

#from .forms import FileForm


class FileAddView(CreateView):
    """
    table view
    """
    model = get_model_from_cfg('DOCUMENT')
    form_class = modelform_factory(get_model_from_cfg('DOCUMENT'), fields=('file',))

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if not self.request.user.has_perms(self.get_permissions([])):
            return permission_denied(self.request)
        return super(FileAddView, self).dispatch(*args, **kwargs)

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
        if not hasattr(self.related_model, '_erpmeta'):
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
            activity_addfile.send(sender=ct.model_class(), instance=ct.model_class().objects.get(pk=pk), file=self.object)
        return HttpResponseRedirect(self.get_success_url())

    def get_rel_object(self):
        if hasattr(self, 'related_object'):
            return self.related_object
        try:
            self.related_object = self.get_rel_model().objects.get(pk=self.kwargs['pk'])
        except self.get_rel_model().DoesNotExist:
            raise Http404

        return self.related_object

    def get_permissions(self, perms):
        info = self.get_rel_model()._meta.app_label, self.get_rel_model()._meta.model_name
        perms.append('%s.view_%s' % info)
        return perms

    def get_success_url(self):
        return self.get_rel_object().erpmodule_detail()
