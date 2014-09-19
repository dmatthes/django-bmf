#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.views.generic import DetailView
from django.utils import six
from django.utils.encoding import force_text

from ..models import Dashboard
from ..viewmixins import ViewMixin


class DashboardView(ViewMixin, DetailView):
    context_object_name = 'object'
    model = Dashboard
    template_name = "djangobmf/dashboard/detail.html"

    def get_object(self):
        # Call the superclass
        if "pk" in self.kwargs:
            self.object = Dashboard.objects.get(user=self.request.user, pk=self.kwargs['pk'])
        else:
            self.object = Dashboard.objects.get_or_create(user=self.request.user, name=None)
        return self.object

    def get_context_data(self, **kwargs):
        if self.kwargs.get('pk', None):
            if self.request.session['djangobmf'].get('dashboard_current', None):
                if self.request.session['djangobmf']['dashboard_current'].get('pk', None) != self.kwargs['pk']:
                    self.update_dashboard(self.kwargs['pk'])
            else:
                self.update_dashboard(self.kwargs['pk'])
        context = super(DashboardView, self).get_context_data(**kwargs)

        from ..sites import site
        models = []
        for ct, model in six.iteritems(site.models):
            info = model._meta.app_label, model._meta.model_name
            perm = '%s.view_%s' % info
            if self.request.user.has_perms([perm, ]):
                # key = unicode(model._bmfmeta.category)
                key = force_text(model._bmfmeta.category)
                models.append({
                    'category': key,
                    'model': model,
                    'name': model._meta.verbose_name_plural,
                    'url': model._bmfmeta.url_namespace + ':index'
                })

        context['modules'] = models
        return context
