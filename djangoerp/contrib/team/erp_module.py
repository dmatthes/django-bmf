#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from djangoerp.sites import site

from .models import Team

from .views import TeamCreateView
from .views import TeamDetailView
from .views import TeamUpdateView

site.register(Team, **{
    'create': TeamCreateView,
    'detail': TeamDetailView,
    'update': TeamUpdateView,
})
