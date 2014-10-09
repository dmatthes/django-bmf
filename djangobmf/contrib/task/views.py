#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.views import ModuleArchiveView
from djangobmf.views import ModuleListView
from djangobmf.views import ModuleLetterView

from djangobmf.views import ModuleDetailView
from djangobmf.views import ModuleCloneView

from .filters import TaskFilter
from .filters import GoalFilter
from .forms import BMFGoalCloneForm


class ArchiveGoalView(ModuleArchiveView):
    slug = "archive"
    name = _("Archive")
    filterset_class = GoalFilter


class ActiveGoalView(ModuleListView):
    slug = "active"
    name = _("Active Goals")
    filterset_class = GoalFilter

    def get_queryset(self):
        return super(ActiveGoalView, self).get_queryset().filter(completed=False)


class MyGoalView(ModuleListView):
    slug = "my"
    name = _("My Goals")

    def get_queryset(self):
        return super(MyGoalView, self).get_queryset() \
            .filter(completed=False, referee=getattr(self.request.user, 'djangobmf_employee', -1))


class ArchiveTaskView(ModuleArchiveView):
    slug = "archive"
    name = _("Archive")
    date_resolution = "month"
    filterset_class = TaskFilter


class OpenTaskView(ModuleLetterView):
    slug = "open"
    name = _("Open Tasks")
    filterset_class = TaskFilter

    def get_queryset(self):
        return super(OpenTaskView, self).get_queryset().filter(completed=False)


class AvailableTaskView(ModuleListView):
    slug = "available"
    name = _("Available Tasks")

    def get_queryset(self):
        return super(AvailableTaskView, self).get_queryset().filter(employee=None, completed=False)


class MyTaskView(ModuleListView):
    slug = "my"
    name = _("My Tasks")

    def get_queryset(self):
        return super(MyTaskView, self).get_queryset() \
            .filter(completed=False, employee=getattr(self.request.user, 'djangobmf_employee', -1))


class TodoTaskView(ModuleListView):
    slug = "todo"
    name = _("Todolist")

    def get_queryset(self):
        return super(TodoTaskView, self).get_queryset() \
            .filter(completed=False, state__in=["todo", "started", "review"],
                    employee=getattr(self.request.user, 'djangobmf_employee', -1))


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
            elif task.state in ["hold", "review", "todo"]:
                tasks["hold"].append(task)
            else:
                tasks["done"].append(task)

        kwargs.update({
            'tasks': tasks,
        })
        return super(GoalDetailView, self).get_context_data(**kwargs)
