#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.conf.urls import patterns, include, url

from .views import ConfigurationView
from .views import ConfigurationEdit

urlpatterns = patterns('',
    url(r'^$', ConfigurationView.as_view(), name="configuration"),
    url(r'^(?P<app_label>[\w_]+)/(?P<name>[\w_]+)/$', ConfigurationEdit.as_view(), name="configuration"),
)
