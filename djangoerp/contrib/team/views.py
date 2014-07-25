#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from djangoerp.views import ModuleCreateView
from djangoerp.views import ModuleUpdateView
from djangoerp.views import ModuleDetailView

from .forms import ERPTeamUpdateForm
from .forms import ERPTeamCreateForm


class TeamCreateView(ModuleCreateView):
    form_class = ERPTeamCreateForm


class TeamUpdateView(ModuleUpdateView):
    form_class = ERPTeamUpdateForm


class TeamDetailView(ModuleDetailView):
    form_class = ERPTeamUpdateForm
