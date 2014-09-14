#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.views.generic import DetailView
# from django.views.generic import UpdateView
# from django.views.generic import CreateView
# from django.views.generic import DeleteView

from django.views.generic import TemplateView
from django.views.generic import RedirectView

# from django.utils import six
# from django.utils.encoding import force_text

from .models import Workspace
from ..viewmixins import ViewMixin


class WorkspaceRedirectView(RedirectView):
    """
    applied to each category. it just redirects to the upper workspace
    """
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        url = self.kwargs['url'].split('/')[:-1]
        return reverse('djangobmf:workspace', None, (), {'url': '/'.join(url)})


class WorkspaceDashboardView(ViewMixin, TemplateView):
    """
    currently a (static) templateview is used
    later this should be a user-defined dashboard with plugins
    """
    template_name = "djangobmf/dashboard/detail.html"


class WorkspaceGenericView(ViewMixin, DetailView):
    context_object_name = 'object'
    model = Workspace
    template_name = "djangobmf/dashboard/detail.html"

    def get_object(self):
        print(self.kwargs)
        return Workspace.objects.all()[0]
