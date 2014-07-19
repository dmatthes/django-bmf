#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.views.generic import ListView
from django.views.generic import UpdateView
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType
from django.utils.text import force_text
from django.http import Http404
from django.http import HttpResponseRedirect

from ..models import Watch
from ..viewmixins import ViewMixin
from ..viewmixins import NextMixin
from ..sites import site

from ..settings import ACTIVITY_WORKFLOW
from ..settings import ACTIVITY_COMMENT
from ..settings import ACTIVITY_UPDATED
from ..settings import ACTIVITY_FILE
from ..settings import ACTIVITY_CREATED

from .forms import WatchDefaultForm, WatchObjectForm


class WatchMixin(object):
    model = Watch

    def get_parent_model(self):
        try:
            return ContentType.objects.get_for_id(int(self.kwargs.get('ct', 0))).model_class()
        except ContentType.DoesNotExist:
            return None

    def get_context_data(self, **kwargs):
        model = self.get_parent_model()

        has_detectchanges = None
        has_files = None
        has_comments = None
        has_workflow = None

        if model:
            if not hasattr(model, '_erpmeta'):
                raise Http404
            if not model._erpmeta.has_activity:
                raise Http404

            has_detectchanges = model._erpmeta.has_detectchanges
            has_files = model._erpmeta.has_files
            has_comments = model._erpmeta.has_comments
            has_workflow = model._erpmeta.has_workflow

        glob = Watch.objects.filter(user=self.request.user, active=True).values('watch_ct').annotate(count=Count('watch_id')).order_by()

        configured = {}
        for d in glob:
            configured[d['watch_ct']] = d['count'] - 1

        navigation = []
        for ct, model in site.models.items():
            if model._erpmeta.has_activity:
                navigation.append({
                    'name': force_text(model._meta.verbose_name_plural),
                    'count': configured.get(ct, 0),
                    'ct': ct,
                })

        kwargs.update({
            'navigation': navigation,
            'selected_ct': int(self.kwargs.get('ct', 0)),

            'has_detectchanges': has_detectchanges,
            'has_files': has_files,
            'has_comments': has_comments,
            'has_workflow': has_workflow,

            'symbols': {
                'workflow': ACTIVITY_WORKFLOW,
                'comment': ACTIVITY_COMMENT,
                'updated': ACTIVITY_UPDATED,
                'file': ACTIVITY_FILE,
                'created': ACTIVITY_CREATED,
            }
        })

        return super(WatchMixin, self).get_context_data(**kwargs)


class WatchView(WatchMixin, ViewMixin, ListView):
    allow_empty = True
    template_name = "djangoerp/watch/index.html"
    paginate_by = 50

    def get_queryset(self):
        qs = super(WatchView, self).get_queryset()
        if not self.kwargs.get('ct', None):
            return []
        return qs.filter(
            user=self.request.user,
            watch_ct_id=self.kwargs.get('ct'),
            watch_id__gt=0,
        ).prefetch_related('watch_object').order_by('-watch_id')

    def get_context_data(self, **kwargs):
        if self.kwargs.get('ct', None):
            if not int(self.kwargs['ct']) in site.models:
                raise Http404

            try:
                default = Watch.objects.get(
                    user=self.request.user,
                    watch_ct_id=self.kwargs.get('ct'),
                    watch_id=0,
                )
            except Watch.DoesNotExist:
                default = Watch()
            kwargs.update({
                'glob_settings': default,
            })
        return super(WatchView, self).get_context_data(**kwargs)


class WatchEdit(WatchMixin, NextMixin, ViewMixin, UpdateView):
    template_name = "djangoerp/watch/edit.html"

    def get_form_class(self):
        if self.kwargs.get('pk', None):
            return WatchObjectForm
        return WatchDefaultForm

    def get_object(self):
        if getattr(self, 'object', None):
            return self.object
        if self.kwargs.get('pk', 0):
            try:
                self.object = self.model.objects.get(user=self.request.user, watch_ct_id=self.kwargs.get('ct'), watch_id=self.kwargs.get('pk'))
            except self.model.DoesNotExist:
                self.object, created = self.model.objects.get_or_create(user=self.request.user, watch_ct_id=self.kwargs.get('ct'), watch_id=0)
                self.object.pk = None
                self.object.watch_id = int(self.kwargs.get('pk'))
                self.object.new_entry = False
                self.object.save()
        else:
            self.object, created = self.model.objects.get_or_create(user=self.request.user, watch_ct_id=self.kwargs.get('ct'), watch_id=0)
        return self.object

    def get_success_url(self):
        return self.redirect_next('djangoerp:watch', ct=self.kwargs['ct'])

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())
