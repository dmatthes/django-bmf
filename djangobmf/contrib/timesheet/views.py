#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from djangobmf.views import ModuleCreateView
from djangobmf.views import ModuleUpdateView
from djangobmf.views import ModuleArchiveView

from .forms import TimesheetCreateForm
from .forms import TimesheetUpdateForm


class ArchiveView(ModuleArchiveView):
    date_resolution = 'week'


class CreateView(ModuleCreateView):
    form_class = TimesheetCreateForm


class UpdateView(ModuleUpdateView):
    form_class = TimesheetUpdateForm
