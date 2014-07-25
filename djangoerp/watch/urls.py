#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .views import WatchView
from .views import WatchEdit

urlpatterns = patterns(
    '',
    url(r'^$', WatchView.as_view(), name="watch"),
    url(r'^(?P<ct>[0-9]+)/$', WatchView.as_view(), name="watch"),
    url(r'^(?P<ct>[0-9]+)/edit/$', WatchEdit.as_view(), name="watch_edit", kwargs={'pk': 0}),
    url(r'^(?P<ct>[0-9]+)/edit/(?P<pk>[0-9]+)/$', WatchEdit.as_view(), name="watch_edit"),
)
