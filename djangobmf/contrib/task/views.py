#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from ...views import ModuleIndexView
from ...views import ModuleDetailView
from ...views import ModuleCloneView

from .filters import TaskFilter
from .filters import GoalFilter
from .forms import BMFGoalCloneForm


class GoalIndexView(ModuleIndexView):
    filterset_class = GoalFilter


class GoalCloneView(ModuleCloneView):
    form_class = BMFGoalCloneForm

    def clone_object(self, formdata, instance):
        instance.completed = False

    def clone_related_objects(self, formdata, old_object, new_object):
        if formdata['copy_tasks']:
            for task in old_object.task_set.all():
                task.pk = None
                task.goal = new_object
                task.project = new_object.project
                if formdata['clear_employee']:
                    task.employee = None
                task.due_date = None
                task.completed = False
                task.work_date = None
                task.seconds_on = 0
                setattr(task, task._bmfmeta.workflow_field, task._bmfmeta.workflow._default_state_key)
                task.save()


class GoalDetailView(ModuleDetailView):
    def get_context_data(self, **kwargs):
        tasks = {
            'open': [],
            'hold': [],
            'done': [],
        }
        for task in self.object.task_set.all():
            if task.state in ["open", "started", "new"]:
                tasks["open"].append(task)
            elif task.state in ["hold", "review"]:
                tasks["hold"].append(task)
            else:
                tasks["done"].append(task)

        kwargs.update({
            'tasks': tasks,
        })
        return super(GoalDetailView, self).get_context_data(**kwargs)


class TaskIndexView(ModuleIndexView):
    filterset_class = TaskFilter
