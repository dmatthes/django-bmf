#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

"""
This is a normal urlconf. it is imported from djangoerp.sites.site.get_url, where
the module views get appended by an '^module/' expression
"""

from django.conf.urls import patterns, url

from .views import DashboardView
from .views import DashboardUpdate
from .views import DashboardCreate
from .views import DashboardDelete

urlpatterns = patterns('',
    url(r'^(?P<pk>[0-9]+)/$', DashboardView.as_view(), name="dashboard"),
    url(r'^create/$',                DashboardCreate.as_view(), name="dashboard_create"),
    url(r'^(?P<pk>[0-9]+)/update/$', DashboardUpdate.as_view(), name="dashboard_update"),
    url(r'^(?P<pk>[0-9]+)/delete/$', DashboardDelete.as_view(), name="dashboard_delete"),
)
