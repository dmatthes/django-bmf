#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.views.generic import DetailView
from django.views.generic import UpdateView
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.utils import six
from django.utils.encoding import force_text

from ..models import Dashboard
from ..viewmixins import ViewMixin

class DashboardView(ViewMixin, DetailView):
    context_object_name = 'object'
    model = Dashboard
    template_name = "djangoerp/dashboard/detail.html"

    def get_object(self):
        # Call the superclass
        if "pk" in self.kwargs:
            self.object = Dashboard.objects.get(user=self.request.user, pk=self.kwargs['pk'])
        else:
            self.object = Dashboard.objects.get_or_create(user=self.request.user, name=None)
        return self.object

    def get_context_data(self, **kwargs):
        if self.kwargs.get('pk', None):
            if self.request.session['djangoerp'].get('dashboard_current', None):
                if self.request.session['djangoerp']['dashboard_current'].get('pk', None) != self.kwargs['pk']:
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
                # key = unicode(model._erpmeta.category)
                key = force_text(model._erpmeta.category)
                models.append({'category': key, 'model': model, 'name': model._meta.verbose_name_plural, 'url': model._erpmeta.url_namespace + ':index'})

        context['modules'] = models
        return context


class DashboardDelete(ViewMixin, DeleteView):
    model = Dashboard
    template_name = "djangoerp/dashboard/delete.html"

    def get_success_url(self):
        self.update_dashboard()
        return reverse('djangoerp:dashboard')


class DashboardCreate(ViewMixin, CreateView):
    model = Dashboard
    fields = ['name',]
    template_name = "djangoerp/dashboard/create.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(DashboardCreate, self).form_valid(form)

    def get_success_url(self):
        self.update_dashboard()
        return reverse('djangoerp:dashboard')


class DashboardUpdate(ViewMixin, UpdateView):
    model = Dashboard
    fields = ['name',]
    template_name = "djangoerp/dashboard/update.html"

    def get_success_url(self):
        self.update_dashboard()
        return reverse('djangoerp:dashboard', kwargs={'pk': self.object.pk})
