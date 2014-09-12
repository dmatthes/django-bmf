#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from djangobmf.models import BMFModel
from djangobmf.settings import BASE_MODULE
from djangobmf.categories import HR

# from .workflows import TimesheetWorkflow


@python_2_unicode_compatible
class AbstractTimesheet(BMFModel):
    """
    """
#   state = WorkflowField()

    summary = models.CharField(_("Title"), max_length=255, null=True, blank=False, )
    description = models.TextField(_("Description"), null=True, blank=True, )
    start = models.DateTimeField(null=True, blank=False)
    end = models.DateTimeField(null=True, blank=True)

    if BASE_MODULE["PROJECT"]:
        project = models.ForeignKey(
            BASE_MODULE["PROJECT"], null=True, blank=True, on_delete=models.SET_NULL,
        )
    if BASE_MODULE["TASK"]:
        project = models.ForeignKey(
            BASE_MODULE["TASK"], null=True, blank=True, on_delete=models.SET_NULL,
        )

    employee = models.ForeignKey(
        BASE_MODULE["EMPLOYEE"], null=True, blank=True, on_delete=models.SET_NULL,
        related_name="+"
    )

    class Meta(BMFModel.Meta):  # only needed for abstract models
        verbose_name = _('Timesheet')
        verbose_name_plural = _('Timesheets')
        ordering = ['start']
        abstract = True
        permissions = (
            ('can_manage', 'Can manage timesheets'),
        )

    def bmfget_customer(self):
        if self.project:
            return self.project.customer
        return None

    def bmfget_project(self):
        return self.project

    def __str__(self):
        return '%s' % (self.start)

    @classmethod
    def has_permissions(cls, qs, user, obj=None):
        if user.has_perm('%s.can_manage' % cls._meta.app_label, cls):
            return qs
        return qs.filter(employee=getattr(user, 'djangobmf_employee', -1))

    class BMFMeta:
        has_logging = True
        category = HR
        # workflow = TimesheetWorkflow
        # workflow_field = 'state'


class Timesheet(AbstractTimesheet):
    pass
