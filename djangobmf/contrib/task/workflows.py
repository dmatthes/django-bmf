#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now

from math import ceil

from djangoerp.workflows import Workflow, State, Transition
from djangoerp.utils import get_model_from_cfg
from django.core.exceptions import ValidationError


class GoalWorkflow(Workflow):
    class States:
        open = State(_(u"Open"), default=True, delete=False)
        completed = State(_(u"Completed"))

    class Transitions:
        complete = Transition(_("Complete this Goal"), "open", "completed")
        reopen = Transition(_("Reopen this Goal"), "completed", "open")

    def complete(self):
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
    bill_resolution = 5  # minutes

    class States:
        new = State(_(u"New"), True, delete=False)
        open = State(_(u"Open"), delete=False)
        started = State(_(u"Started"), delete=False)
        hold = State(_(u"Hold"), delete=False)
        review = State(_(u"Review"), delete=False, update=False)
        finished = State(_(u"Finished"), update=False, delete=True)
        cancelled = State(_(u"Cancelled"), update=False, delete=True)

    class Transitions:
        start = Transition(
            _("Work on this task"),
            ["new", "hold", "open"],
            "started",
            condition=start_condition,
        )
        hold = Transition(
            _("Set this task on hold"),
            ["new", "open", "started"],
            "hold",
        )
        stop = Transition(
            _("Stop working on this task"),
            "started",
            "open",
        )
        finish = Transition(
            _("Finish this task"),
            ["started", "open", "hold", "new", "review"],
            "finished",
            condition=finish_condition,
        )
        review = Transition(
            _("Set to review"),
            ["started", "open", "hold", "new"],
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
        self.instance.work_date = now()
        if hasattr(self.instance, 'employee'):
            self.instance.employee_id = self.user.pk

    def stop(self):
        if self.instance.work_date:
            self.instance.seconds_on += int((now() - self.instance.work_date).total_seconds())
        self.instance.work_date = now()

    def hold(self):
        self.stop()

    def unreview(self):  # LOOK: probably not needed, if timesheets are implemented
        self.instance.work_date = now()

    def reopen(self):
        self.instance.seconds_on = 0  # LOOK: probably not needed, if timesheets are implemented
        self.instance.work_date = now()
        self.instance.completed = False

    def review(self):
        self.stop()

    def finish(self):
        self.stop()
        self.instance.due_date = None

        # TODO remove this functionality IF timesheets are implemented
        billable_time = ceil(self.instance.seconds_on / 60.)

        # get the project from
        if self.instance.project:  # TODO untested
            project = self.instance.project
        elif self.instance.goal:  # TODO untested
            project = self.instance.goal.project
        else:
            project = None

        self.instance.completed = True

        if project and project.customer and self.instance.goal and self.instance.employee:  # TODO untested
            if self.instance.goal.billable and billable_time > 0:
                if not self.instance.employee.product:
                    raise ValidationError(_("The employee's user-account needs a default product"))
                position = get_model_from_cfg('POSITION')(
                    name=self.instance.summary, project=project,
                    employee=self.user.erp_employee,
                    date=now(), product=self.user.erp_employee.product,
                    amount=self.bill_resolution * ceil(billable_time / self.bill_resolution) / 60.)
                position.clean()
                position.save()
                return position.erpmodule_detail()

    def cancel(self):
        self.finish()
