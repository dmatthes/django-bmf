#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.conf.urls import patterns, url

from djangoerp.sites import site

from .models import Position
from .views import PositionTableView
from .views import PositionDetailView
from .views import PositionUpdateView
from .views import PositionCreateView
from .views import PositionAPI

site.register(Position, **{
    'index':  PositionTableView,
    'create': PositionCreateView,
    'update': PositionUpdateView,
    'detail': PositionDetailView,
    'urlpatterns': patterns('',
        url(r'^api/$', PositionAPI.as_view(), name="api"),
    ),
})
