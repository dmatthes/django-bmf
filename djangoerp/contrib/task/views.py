#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.db.models import Count

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

    def get_queryset(self):
        qs = super(TaskIndexView, self).get_queryset()
        qs = qs.annotate(null_count=Count('due_date')).order_by('-null_count','due_date','summary')
        return qs
