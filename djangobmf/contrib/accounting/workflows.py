#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.workflows import Workflow, State, Transition


class TransactionWorkflow(Workflow):
    class States:
        open = State(_(u"Open"), True, delete=False)
        balanced = State(_(u"Balanced"), update=False, delete=False)
        cancelled = State(_(u"Cancelled"), update=False, delete=False)

    class Transitions:
        balance = Transition(_("Balance"), "open", "balanced")
        cancel = Transition(_("Cancel"), "open", "cancelled", validate=False)
