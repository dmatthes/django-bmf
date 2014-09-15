#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now

from djangobmf.workflows import Workflow, State, Transition


def validate_condition(object, user):
    if user.has_perm('djangobmf_timesheet.can_manage', object):
        return True
    return False


class TimesheetWorkflow(Workflow):

    class States:
        active = State(_(u"Active"), True, update=False, delete=False)
        finished = State(_(u"Finished"), delete=True)
        validated = State(_(u"Validated"), update=False, delete=True)

    class Transitions:
        finish = Transition(
            _("Finish"),
            ["active"],
            "finished",
        )
        validate = Transition(
            _("Validate"),
            ["finished"],
            "validated",
            condition=validate_condition,
        )

    def finish(self):
        self.instance.end = now()

    def validate(self):
        self.validated = True
