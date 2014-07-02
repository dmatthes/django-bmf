#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.contrib import admin
from django.conf import settings

from .configuration.models import Configuration
admin.site.register(Configuration)

from .dashboard.models import Dashboard
admin.site.register(Dashboard)

from .numbering.models import NumberCycle
admin.site.register(NumberCycle)

from .report.models import Report
admin.site.register(Report)

from .dashboard.models import View
admin.site.register(View)

from .watch.models import Watch
admin.site.register(Watch)
