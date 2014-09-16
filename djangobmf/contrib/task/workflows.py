#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from djangobmf.workflows import Workflow, State, Transition
from djangobmf.settings import CONTRIB_TIMESHEET
from djangobmf.utils.model_from_name import model_from_name


def cancel_condition(object, user):
    if getattr(object, 'referee_id', False) and object.referee_id != user.pk:
        return False
    return True


class GoalWorkflow(Workflow):
    class States:
        open = State(_(u"Open"), default=True, delete=False)
        completed = State(_(u"Completed"), update=False, delete=True)
        cancelled = State(_(u"Cancelled"), update=False, delete=True)

    class Transitions:
        complete = Transition(_("Complete this Goal"), "open", "completed")
        cancel = Transition(_("Cancel this Goal"), "open", "cancelled", condition=cancel_condition)
        reopen = Transition(_("Reopen this Goal"), ["completed", "cancelled"], "open")

    def complete(self):
        if self.instance.task_set.filter(completed=False).count() > 0:  # TODO untested
            raise ValidationError(_('You can not complete a goal which has open tasks'))
        self.instance.completed = True

    def cancel(self):
        # TODO autoclose all tasks
        if self.instance.task_set.filter(completed=False).count() > 0:  # TODO untested
            raise ValidationError(_('You can not complete a goal which has open tasks'))
        self.instance.completed = True

    def reopen(self):
        self.instance.completed = False


def start_condition(object, user):
    if getattr(object, 'employee_id', False) and object.employee_id != user.pk:  # TODO: untested
        return False
    return True


def finish_condition(object, user):
    if object.goal and object.goal.referee_id and user.pk != object.goal.referee_id:  # TODO: untested
        return False
    return True


class TaskWorkflow(Workflow):

    class States:
        new = State(_(u"New"), True, delete=False)
        open = State(_(u"Open"), delete=False)
        hold = State(_(u"Hold"), delete=False)
        todo = State(_(u"Todo"), delete=False)
        started = State(_(u"Started"), delete=False)
        review = State(_(u"Review"), delete=False, update=False)
        finished = State(_(u"Finished"), update=False, delete=True)
        cancelled = State(_(u"Cancelled"), update=False, delete=True)

    class Transitions:
        start = Transition(
            _("Work on this task"),
            ["new", "hold", "open", "todo"],
            "started",
            condition=start_condition,
        )
        todo = Transition(
            _("Mark as todo"),
            ["new", "open", "started", "hold"],
            "todo",
        )
        hold = Transition(
            _("Set this task on hold"),
            ["new", "open", "started", "todo"],
            "hold",
        )
        stop = Transition(
            _("Stop working on this task"),
            "started",
            "open",
        )
        finish = Transition(
            _("Finish this task"),
            ["started", "open", "hold", "new", "review", "todo"],
            "finished",
            condition=finish_condition,
        )
        review = Transition(
            _("Set to review"),
            ["started", "open", "hold", "new", "todo"],
            "review",
        )
        reopen = Transition(
            _("Reopen this task"),
            ['finished', 'cancelled'],
            'open',
        )
        unreview = Transition(
            _("Reopen this task"),
            ['review'],
            'open',
        )
        cancel = Transition(
            _("Cancel this task"),
            ('new', 'hold', 'open', 'review'),
            'cancelled',
            condition=finish_condition,
        )

    def start(self):
        self.instance.in_charge = self.user.djangobmf_employee
        self.instance.employee = self.user.djangobmf_employee

        if self.instance.project:
            project = self.instance.project
        elif self.instance.goal:
            project = self.instance.goal.project
        else:
            project = None

        timesheet = model_from_name(CONTRIB_TIMESHEET)
        if timesheet is not None:
            obj = timesheet(
                task=self.instance,
                employee=self.user.djangobmf_employee,
                auto=True,
                project=project,
                summary=self.instance.summary
            )
            obj.save()

    def todo(self):
        self.instance.in_charge = self.user.djangobmf_employee
        self.instance.employee = self.user.djangobmf_employee

    def stop(self):
        if not self.instance.in_charge and self.instance.employee:
            self.instance.in_charge = self.instance.employee

        timesheet = model_from_name(CONTRIB_TIMESHEET)
        if timesheet is not None:
            for obj in timesheet.objects.filter(
                task=self.instance,
                employee__in=[self.instance.in_charge, self.user.djangobmf_employee],
                end=None,
                auto=True,
            ):
                obj.bmfworkflow_transition('finish', self.user)

    def hold(self):
        self.stop()

    def unreview(self):
        self.instance.employee = self.instance.in_charge

    def reopen(self):
        self.instance.employee = self.instance.in_charge
        self.instance.completed = False

    def review(self):
        if not self.instance.in_charge and self.instance.employee:
            self.instance.in_charge = self.instance.employee
        if self.instance.goal:
            self.instance.employee = self.instance.goal.referee
        self.stop()

    def finish(self):
        self.stop()
        self.instance.due_date = None
        self.instance.completed = True

    def cancel(self):
        self.finish()
