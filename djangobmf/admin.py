#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .configuration.models import Configuration
from .dashboard.models import Dashboard
from .numbering.models import NumberCycle
from .report.models import Report
from .workspace.models import Workspace


admin.site.register(Configuration)
admin.site.register(Dashboard)
admin.site.register(NumberCycle)
admin.site.register(Report)


class WorkspaceAdmin(MPTTModelAdmin):
    list_display = ('slug', 'type', 'ct', 'public', 'editable', 'url', 'lft', 'rght', 'level', 'tree_id')

admin.site.register(Workspace, WorkspaceAdmin)
