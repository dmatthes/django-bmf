#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .views import FileAddView

urlpatterns = patterns('',
    url(r'^add/(?P<ct>[0-9]+)/(?P<pk>[0-9]+)/$', FileAddView.as_view(), name="file_add"),
)
