#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from djangobmf.sites import site

from .models import Timesheet

site.register(Timesheet, **{
})
