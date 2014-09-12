#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .views import NotificationView
from .views import NotificationUpdate
from .views import ActivityView
from .views import HistoryCommentAddView
from .views import ActivityView as HistoryCommentGetView


urlpatterns = patterns(
    '',
    url(
        r'^$', NotificationView.as_view(), name="notification", kwargs={'filter': "unread", 'ct': 0},
    ),
    url(
        r'^(?P<filter>all|active)/$', NotificationView.as_view(), name="notification", kwargs={'ct': 0},
    ),
    url(
        r'^(?P<filter>all|active|unread)/(?P<ct>[0-9]+)/$', NotificationView.as_view(), name="notification",
    ),
    url(
        r'^edit/(?P<pk>[0-9]+)/$', NotificationUpdate.as_view(), name="notification-edit",
    ),
    url(
        r'^activity/$', ActivityView.as_view(), name="activity",
    ),
    url(
        r'^comment/get/(?P<ct>[0-9]+)/(?P<pk>[0-9]+)/$',
        HistoryCommentGetView.as_view(), name="activity_comment_get",
    ),
    url(
        r'^comment/add/(?P<ct>[0-9]+)/(?P<pk>[0-9]+)/$',
        HistoryCommentAddView.as_view(), name="activity_comment_add",
    ),
)
