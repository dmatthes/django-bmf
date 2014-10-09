#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.conf.urls import patterns, url
from django.utils.translation import ugettext_lazy as _

from djangobmf.categories import BaseCategory
from djangobmf.categories import Sales
from djangobmf.sites import site

from .models import Position
from .views import OpenPositionView
from .views import AllPositionView
from .views import PositionTableView
from .views import PositionDetailView
from .views import PositionUpdateView
from .views import PositionCreateView
from .views import PositionAPI

site.register(Position, **{
    'index': PositionTableView,
    'create': PositionCreateView,
    'update': PositionUpdateView,
    'detail': PositionDetailView,
    'urlpatterns': patterns(
        '',
        url(r'^api/$', PositionAPI.as_view(), name="api"),
    ),
})


class PositionCategory(BaseCategory):
    name = _('Positions')
    slug = "positions"


site.register_dashboard(Sales)
site.register_category(Sales, PositionCategory)
site.register_view(Position, PositionCategory, OpenPositionView)
site.register_view(Position, PositionCategory, AllPositionView)
