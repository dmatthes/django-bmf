#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from .views import ActivityView
from .views import HistoryCommentAddView
from .views import ActivityView as HistoryCommentGetView

urlpatterns = patterns('',
    url(r'^$', ActivityView.as_view(), name="activity"),
    url(r'^comment/get/(?P<ct>[0-9]+)/(?P<pk>[0-9]+)/$', HistoryCommentGetView.as_view(), name="activity_comment_get"),
    url(r'^comment/add/(?P<ct>[0-9]+)/(?P<pk>[0-9]+)/$', HistoryCommentAddView.as_view(), name="activity_comment_add"),
)
