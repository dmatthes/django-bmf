#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.sites import site
from djangobmf.categories import BaseCategory
from djangobmf.categories import ProjectManagement

from .models import Task
from .models import Goal

from .views import TaskIndexView
from .views import GoalCloneView
from .views import GoalIndexView
from .views import GoalDetailView


site.register(Task, **{
    'index': TaskIndexView,
})

site.register(Goal, **{
    'index': GoalIndexView,
    'clone': GoalCloneView,
    'detail': GoalDetailView,
})


class GoalCategory(BaseCategory):
    name = _('Goals')
    slug = "goals"


class TaskCategory(BaseCategory):
    name = _('tasks')
    slug = "tasks"

site.register_dashboard(ProjectManagement)

site.register_category(ProjectManagement, GoalCategory)
site.register_view(Goal, GoalCategory, GoalIndexView)

site.register_category(ProjectManagement, TaskCategory)
