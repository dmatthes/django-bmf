#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

"""
This is a normal urlconf. it is imported from djangobmf.sites.site.get_url, where
the module views get appended by an '^module/' expression
"""

from django.conf.urls import patterns, url

from .views import DashboardView

urlpatterns = patterns(
    '',
    url(
        r'^(?P<pk>[0-9]+)/$', DashboardView.as_view(), name="dashboard",
    ),
)
