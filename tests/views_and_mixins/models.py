#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.db import models

from djangobmf.models import BMFModel
from djangobmf.fields import WorkflowField
from djangobmf.workflows import Workflow, State, Transition


class TestWorkflow(Workflow):
    class States:
        start = State("start", default=True, delete=False)
        end = State("end", update=False, delete=True)

    class Transitions:
        go = Transition("go", "start", "end")


class TestView(BMFModel):
    state = WorkflowField()
    field = models.CharField(max_length=3)

    class BMFMeta:
        has_files = True
        has_comments = True
        observed_fields = ['field', ]
        workflow = TestWorkflow
        workflow_field = 'state'
