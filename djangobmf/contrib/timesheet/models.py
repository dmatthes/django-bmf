#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from djangobmf.models import BMFModel
from djangobmf.fields import WorkflowField
from djangobmf.fields import OptionalForeignKey
from djangobmf.settings import BASE_MODULE
from djangobmf.categories import HR

from .workflows import TimesheetWorkflow


@python_2_unicode_compatible
class AbstractTimesheet(BMFModel):
    """
    """
    state = WorkflowField()

    summary = models.CharField(_("Title"), max_length=255, null=True, blank=False, )
    description = models.TextField(_("Description"), null=True, blank=True, )
    start = models.DateTimeField(null=True, blank=False, default=now)
    end = models.DateTimeField(null=True, blank=True)
    valid = models.BooleanField(default=False, editable=False)

    employee = models.ForeignKey(
        BASE_MODULE["EMPLOYEE"], null=True, blank=True, on_delete=models.SET_NULL,
        related_name="+"
    )

    project = OptionalForeignKey(
        BASE_MODULE["PROJECT"], null=True, blank=True, on_delete=models.SET_NULL,
    )

    task = OptionalForeignKey(
        BASE_MODULE["TASK"], null=True, blank=True, on_delete=models.SET_NULL,
    )

    def clean(self):
        # overwrite the project with the goals project
        if self.task:
            self.project = self.task.project

    def get_project_queryset(self, qs):
        if self.task:
            return qs.filter(task=self.task)
        else:
            return qs

    def get_task_queryset(self, qs):
        if self.project:
            return qs.filter(project=self.project)
        else:
            return qs

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
        workflow = TimesheetWorkflow
        workflow_field = 'state'


class Timesheet(AbstractTimesheet):
    pass
