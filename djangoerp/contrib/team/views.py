#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from .models import Team

from djangoerp.views import PluginCreate
from djangoerp.views import PluginUpdate
from djangoerp.views import PluginDetail

from .forms import ERPTeamUpdateForm
from .forms import ERPTeamCreateForm


class TeamCreateView(PluginCreate):
    form_class = ERPTeamCreateForm


class TeamUpdateView(PluginUpdate):
    form_class = ERPTeamUpdateForm


class TeamDetailView(PluginDetail):
    form_class = ERPTeamUpdateForm
