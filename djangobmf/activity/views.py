#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.generic import CreateView
from django.http import HttpResponseRedirect
from django.http import Http404
from django.views.defaults import permission_denied
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now

from ..models import Activity
from ..models import Notification
from .forms import HistoryCommentForm
from ..signals import activity_comment


class ActivityView(ListView):
    """
    table view
    """
    model = Notification
    allow_empty = True
    template_name = "djangobmf/activity_list.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ActivityView, self).dispatch(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        qs = super(ActivityView, self).get_queryset(*args, **kwargs)
        return qs.filter(user=self.request.user).select_related('history', 'ct')


class HistoryCommentAddView(CreateView):
    """
    table view
    """
    model = Activity
    form_class = HistoryCommentForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if not self.request.user.has_perms(self.get_permissions([])):
            return permission_denied(self.request)
        return super(HistoryCommentAddView, self).dispatch(*args, **kwargs)

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

    def form_valid(self, form):
        if form.instance.text or form.instance.topic:
            form.instance.user = self.request.user
            form.instance.parent_id = self.kwargs['pk']
            form.instance.parent_ct = ContentType.objects.get_for_id(self.kwargs['ct'])
            self.object = form.save()
            self.object.parent_object.modified = now()
            self.object.parent_object.modified_by = self.request.user
            self.object.parent_object.save()
            activity_comment.send(sender=self.object.__class__, instance=self.object)
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
        return self.get_rel_object().bmfmodule_detail()
