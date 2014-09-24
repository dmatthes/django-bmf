#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .views import DocumentCreateView
from .views import DocumentDownloadView

urlpatterns = patterns(
    '',
    url(
        r'^add/(?P<ct>[0-9]+)/(?P<pk>[0-9]+)/$', DocumentCreateView.as_view(), name="document-add",
    ),
    url(
        r'^get/(?P<pk>[0-9]+)/$', DocumentDownloadView.as_view(), name="document-get",
    ),
)
