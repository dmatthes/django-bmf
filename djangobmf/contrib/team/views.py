#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from djangobmf.views import ModuleCreateView
from djangobmf.views import ModuleUpdateView
from djangobmf.views import ModuleDetailView

from .forms import BMFTeamUpdateForm
from .forms import BMFTeamCreateForm


class TeamCreateView(ModuleCreateView):
    form_class = BMFTeamCreateForm


class TeamUpdateView(ModuleUpdateView):
    form_class = BMFTeamUpdateForm


class TeamDetailView(ModuleDetailView):
    form_class = BMFTeamUpdateForm
