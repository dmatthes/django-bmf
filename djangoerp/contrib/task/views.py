#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from djangoerp.views import PluginIndex
from djangoerp.views import PluginDetail

from .models import Task
from .filters import TaskFilter
from .filters import GoalFilter


class GoalIndexView(PluginIndex):
    filterset_class = GoalFilter


class GoalDetailView(PluginDetail):
    def get_context_data(self, **kwargs):
        tasks = {
            'open': [],
            'hold': [],
            'done': [],
        }
        for task in self.object.task_set.all():
            if task.state in ["open", "started","new"]:
                tasks["open"].append(task)
            elif task.state in ["hold", "review"]:
                tasks["hold"].append(task)
            else:
                tasks["done"].append(task)

        kwargs.update({
            'tasks': tasks,
        })
        return super(GoalDetailView, self).get_context_data(**kwargs)

class TaskIndexView(PluginIndex):
    filterset_class = TaskFilter
