#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .views import FileAddView
from .views import FileDownloadView

urlpatterns = patterns(
    '',
    url(
        r'^download/(?P<pk>[0-9]+)/$', FileDownloadView.as_view(), name="file_download",
    ),
    url(
        r'^add/(?P<ct>[0-9]+)/(?P<pk>[0-9]+)/$', FileAddView.as_view(), name="file_add",
    ),
)
