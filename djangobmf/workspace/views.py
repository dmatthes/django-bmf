#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.http import Http404
# from django.views.generic import View
from django.views.generic import DetailView
# from django.views.generic import UpdateView
# from django.views.generic import CreateView
# from django.views.generic import DeleteView
# from django.views.generic import TemplateView
from django.views.generic import RedirectView

from djangobmf.viewmixins import ViewMixin
from djangobmf.views import ModuleGenericListView

from .models import Workspace


class WorkspaceRedirectView(RedirectView):
    """
    applied to each category. it just redirects to the upper workspace
    """
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        url = self.kwargs['url'].split('/')[:-1]
        return reverse('djangobmf:workspace', None, (), {'url': '/'.join(url)})


class WorkspaceDashboardView(ViewMixin, DetailView):
    """
    currently a (static) templateview is used
    later this should be a user-defined dashboard with plugins
    """
    template_name = "djangobmf/dashboard/detail.html"

    def get_object(self):
        try:
            obj = Workspace.objects.get(url=self.kwargs['url'])
        except Workspace.DoesNotExist:
            raise Http404
        self.workspace = obj
        return obj


def workspace_generic_view(request, *args, **kwargs):
    try:
        obj = Workspace.objects.get(url=kwargs['url'])
    except Workspace.DoesNotExist:
        raise Http404

    if not obj.module_cls:
        # TODO add logging
        raise Http404

    if not issubclass(obj.module_cls, ModuleGenericListView):
        raise ImproperlyConfigured("%s must be a subclass of ModuleGenericListView" % obj.module)

    response_function = obj.module_cls.as_view(
        model=obj.ct.model_class(),
        workspace=obj,
    )

    return response_function(request, *args, **kwargs)
