#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.core.urlresolvers import resolve
from django.views.generic import DetailView
from django.views.generic import UpdateView
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import RedirectView
from django.utils import six
from django.utils.encoding import force_text

from .models import Workspace
from ..viewmixins import ViewMixin


class WorkspaceView(ViewMixin, DetailView):
    context_object_name = 'object'
    model = Workspace
    template_name = "djangobmf/dashboard/detail.html"

    def get_object(self):
        print(self.kwargs)
        return Workspace.objects.all()[0]


class WorkspaceRedirectView(RedirectView):
    def get_redirect_url(self, **kwargs):
        url = self.kwargs['url'].split('/')[:-1]
        return reverse('djangobmf:workspace', None, (), {'url': '/'.join(url)})


class WorkspaceDashboardView(WorkspaceView):
    pass


class WorkspaceGenericView(WorkspaceView):
    pass
