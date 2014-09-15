#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from djangobmf.sites import site

from .models import Timesheet

from .views import CreateView
from .views import UpdateView

site.register(Timesheet, **{
    'create': CreateView,
    'update': UpdateView,
})
