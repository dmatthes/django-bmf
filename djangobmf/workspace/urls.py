#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .views import WorkspaceDashboardView
from .views import WorkspaceRedirectView
from .views import workspace_generic_view


urlpatterns = patterns(
    '',
    url(
        r'^$',
        WorkspaceDashboardView.as_view(),
        name="workspace",
    ),
    url(
        r'^(?P<url>(?P<slug1>[\w-]+))/$',
        WorkspaceDashboardView.as_view(),
        name="workspace",
    ),
    url(
        r'^(?P<url>(?P<slug1>[\w-]+)/(?P<slug2>[\w-]+))/$',
        WorkspaceRedirectView.as_view(),
        name="workspace",
    ),
    url(
        r'^(?P<url>(?P<slug1>[\w-]+)/(?P<slug2>[\w-]+)/(?P<slug3>[\w-]+))/$',
        workspace_generic_view,
        name="workspace",
    ),
)
