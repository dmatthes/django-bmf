#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

"""
This is a normal urlconf. it is imported from djangoerp.sites.site.get_url, where
the module views get appended by an '^module/' expression
"""

from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView
from django.views.generic.base import TemplateView
from django.contrib.auth.views import logout
from django.conf import settings
from django.utils.importlib import import_module
from django.utils.module_loading import module_has_submodule

from djangoerp.dashboard.views import DashboardView
from djangoerp.module.views import ModuleView
from djangoerp.modals.views import ModalSaveView

urlpatterns = patterns('',
    url(r'^$', DashboardView.as_view(), name="dashboard"),
    url(r'^accounts/', include('djangoerp.account.urls')),
    url(r'^config/', include('djangoerp.configuration.urls')),
    url(r'^dashboard/', include('djangoerp.dashboard.urls')),
#   url(r'^messages/', include('djangoerp.message.urls')),
    url(r'^notifications/', include('djangoerp.notification.urls')),
    url(r'^watching/', include('djangoerp.watch.urls')),
    url(r'^wizard/', include('djangoerp.wizard.urls')),
    #   r'^module/' via sites

    # TODO
    url(r'^modules/$', ModuleView.as_view(), name="modules"),
    url(r'^ajax/save/view/$', ModalSaveView.as_view(), name="modal_saveview"),
    url(r'^activities/', include('djangoerp.activity.urls')),
    url(r'^file/', include('djangoerp.file.urls')),
)
