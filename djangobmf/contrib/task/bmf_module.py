#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.sites import site
from djangobmf.categories import BaseCategory
from djangobmf.categories import ProjectManagement

from .models import Task
from .models import Goal

from .views import ArchiveTaskView
from .views import AvailableTaskView
from .views import MyTaskView
from .views import OpenTaskView
from .views import TodoTaskView

from .views import ActiveGoalView
from .views import ArchiveGoalView
from .views import MyGoalView

from .views import GoalCloneView
from .views import GoalDetailView


site.register(Task, **{
    'index': ArchiveTaskView,
})

site.register(Goal, **{
    'index': ArchiveGoalView,
    'clone': GoalCloneView,
    'detail': GoalDetailView,
})


class GoalCategory(BaseCategory):
    name = _('Goals')
    slug = "goals"


class TaskCategory(BaseCategory):
    name = _('Tasks')
    slug = "tasks"

site.register_dashboard(ProjectManagement)

site.register_category(ProjectManagement, GoalCategory)
site.register_view(Goal, GoalCategory, MyGoalView)
site.register_view(Goal, GoalCategory, ActiveGoalView)
site.register_view(Goal, GoalCategory, ArchiveGoalView)

site.register_category(ProjectManagement, TaskCategory)
site.register_view(Task, TaskCategory, MyTaskView)
site.register_view(Task, TaskCategory, TodoTaskView)
site.register_view(Task, TaskCategory, AvailableTaskView)
site.register_view(Task, TaskCategory, OpenTaskView)
site.register_view(Task, TaskCategory, ArchiveTaskView)
