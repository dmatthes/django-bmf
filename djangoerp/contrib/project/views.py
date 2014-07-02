#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from djangoerp.views import PluginCreate, PluginUpdate

from .forms import ProjectUpdateForm


class ProjectUpdateView(PluginUpdate):
    pass
