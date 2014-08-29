#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

import django_filters

from djangobmf.filters import HasValueFilter

from .models import Task
from .workflows import TaskWorkflow

from .models import Goal


class TaskFilter(django_filters.FilterSet):
    due_date = HasValueFilter()
    state = django_filters.MultipleChoiceFilter(choices=TaskWorkflow()._states.items())

    class Meta:
        model = Task
        fields = ['project', 'employee', 'state']


class GoalFilter(django_filters.FilterSet):

    class Meta:
        model = Goal
        fields = ['project', 'referee', 'completed']
