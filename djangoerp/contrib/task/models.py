#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.db import models
from django.db.models import Q
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from djangoerp.models import ERPModel
from djangoerp.fields import WorkflowField
from djangoerp.settings import BASE_MODULE
from django.utils.timezone import now
from djangoerp.categories import PROJECT

from .workflows import GoalWorkflow
from .workflows import TaskWorkflow

from math import floor


class GoalManager(models.Manager):

    def get_queryset(self):

        if BASE_MODULE["PROJECT"]:
            return super(GoalManager, self).get_queryset().select_related('project')
        return super(GoalManager, self).get_queryset()


@python_2_unicode_compatible
class AbstractGoal(ERPModel):
    """
    """
    state = WorkflowField()

    summary = models.CharField(_("Title"), max_length=255, null=True, blank=False, )
    description = models.TextField(_("Description"), null=True, blank=True, )

    if BASE_MODULE["PROJECT"]:
        project = models.ForeignKey(
            BASE_MODULE["PROJECT"], null=True, blank=True, on_delete=models.CASCADE,
        )

    referee = models.ForeignKey(
        BASE_MODULE["EMPLOYEE"], null=True, blank=True, on_delete=models.SET_NULL,
        related_name="+"
    )
    team = models.ForeignKey(
        BASE_MODULE["TEAM"], null=True, blank=True, on_delete=models.SET_NULL,
    )
    employees = models.ManyToManyField(
        BASE_MODULE["EMPLOYEE"], null=True, blank=True,
        related_name="employees"
    )

    billable = models.BooleanField(_("Is billable"), default=False)
    completed = models.BooleanField(_("Completed"), default=False, editable=False)

    objects = GoalManager()

    class Meta(ERPModel.Meta):  # only needed for abstract models
        verbose_name = _('Goal')
        verbose_name_plural = _('Goals')
        ordering = ['project__name', 'summary']
        abstract = True
        permissions = (
            ('can_manage', 'Can manage all goals'),
        )

    def erpget_customer(self):
        if self.project:
            return self.project.customer
        return None

    def erpget_project(self):
        return self.project

    @staticmethod
    def erprelated_project_queryset(qs):
        return qs.filter(completed=False)

    def __str__(self):
        return '%s' % (self.summary)

    @classmethod
    def has_permissions(cls, qs, user, obj=None):
        if user.has_perm('%s.can_manage' % cls._meta.app_label, cls):
            return qs

        qs_filter = Q(referee=getattr(user, 'djangoerp_employee', -1))
        qs_filter |= Q(employees=getattr(user, 'djangoerp_employee', -1))
        qs_filter |= Q(team__in=getattr(user, 'djangoerp_teams', []))

        if hasattr(cls, "project"):
            project = cls._meta.get_field_by_name("project")[0].model
            if user.has_perm('%s.can_manage' % project._meta.app_label, project):
                qs_filter |= Q(project__isnull=False)
            else:
                qs_filter |= Q(project__isnull=False, project__employees=getattr(user, 'djangoerp_employee', -1))
                qs_filter |= Q(project__isnull=False, project__team__in=getattr(user, 'djangoerp_teams', []))
        return qs.filter(qs_filter)

    def get_states(self):
        active_states = 0
        states = {
            "hold": 0.,
            "review": 0.,
            "done": 0.,
        }

        for state, count in self.task_set.values_list('state').annotate(count=models.Count('state')).order_by():
            if state in ["new", "open", "started", ]:
                active_states += count

            if state in ["hold", ]:
                states["hold"] += count
                active_states += count

            if state in ["review", ]:
                states["review"] += count
                active_states += count

            if state in ["finished", ]:
                states["done"] += count
                active_states += count

        if active_states == 0:
            return states

        states['hold'] = '%4.2f' % (floor(10000 * states["hold"] / active_states) / 100)
        states['done'] = '%4.2f' % (floor(10000 * states["done"] / active_states) / 100)
        states['review'] = '%4.2f' % (floor(10000 * states["review"] / active_states) / 100)

        return states

    class ERPMeta:
        has_logging = False
        category = PROJECT
        workflow = GoalWorkflow
        workflow_field = 'state'
        can_clone = True


class Goal(AbstractGoal):
    pass


class TaskManager(models.Manager):

    def get_queryset(self):

        related = ['goal']
        if BASE_MODULE["PROJECT"]:
            related.append('project')

        return super(TaskManager, self).get_queryset() \
            .annotate(due_count=models.Count('due_date')) \
            .order_by('-due_count', 'due_date', 'summary') \
            .select_related(*related)


@python_2_unicode_compatible
class AbstractTask(ERPModel):
    """
    """

    state = WorkflowField()

    summary = models.CharField(_("Title"), max_length=255, null=True, blank=False)
    description = models.TextField(_("Description"), null=True, blank=True)

    due_date = models.DateField(_('Due date'), null=True, blank=True)

    work_date = models.DateTimeField(null=True, editable=False)

    project = models.ForeignKey(
        BASE_MODULE["PROJECT"], null=True, blank=True, on_delete=models.CASCADE,
    )
    employee = models.ForeignKey(
        BASE_MODULE["EMPLOYEE"], null=True, blank=True, on_delete=models.SET_NULL,
    )

    goal = models.ForeignKey(BASE_MODULE["GOAL"], null=True, blank=True, on_delete=models.CASCADE)

    seconds_on = models.PositiveIntegerField(null=True, default=0, editable=False)
    completed = models.BooleanField(_("Completed"), default=False, editable=False)

    objects = TaskManager()

    class Meta(ERPModel.Meta):  # only needed for abstract models
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')
        ordering = ['due_date', 'summary']
        abstract = True

    def __str__(self):
        return '#%s: %s' % (self.pk, self.summary)

    @classmethod
    def has_permissions(cls, qs, user, obj=None):
        qs_filter = Q(project__isnull=True, goal__isnull=True)
        qs_filter |= Q(employee=getattr(user, 'djangoerp_employee', -1))

        if hasattr(cls, "goal"):
            goal = cls._meta.get_field_by_name("goal")[0].model
            if user.has_perm('%s.can_manage' % goal._meta.app_label, goal):
                qs_filter |= Q(goal__isnull=False)
            else:
                qs_filter |= Q(goal__isnull=False, goal__referee=getattr(user, 'djangoerp_employee', -1))
                qs_filter |= Q(goal__isnull=False, goal__employees=getattr(user, 'djangoerp_employee', -1))
                qs_filter |= Q(goal__isnull=False, goal__team__in=getattr(user, 'djangoerp_teams', []))

        if hasattr(cls, "project"):
            project = cls._meta.get_field_by_name("project")[0].model
            if user.has_perm('%s.can_manage' % project._meta.app_label, project):
                qs_filter |= Q(project__isnull=False)
            else:
                qs_filter |= Q(project__isnull=False, project__employees=getattr(user, 'djangoerp_employee', -1))
                qs_filter |= Q(project__isnull=False, project__team__in=getattr(user, 'djangoerp_teams', []))

        return qs.filter(qs_filter)

    def clean(self):
        # overwrite the project with the goals project
        if self.goal:
            self.project = self.goal.project

    def get_project_queryset(self, qs):
        if self.goal:
            return qs.filter(goal=self.goal)
        else:
            return qs

    def get_goal_queryset(self, qs):
        if self.project:
            return qs.filter(project=self.project)
        else:
            return qs

    def due_days(self):
        if self.due_date:
            time = now().date()
            if time >= self.due_date:
                return 0
            return (self.due_date - time).days

    class ERPMeta:
        has_files = True
        has_comments = True
        workflow = TaskWorkflow
        workflow_field = 'state'
        category = PROJECT


class Task(AbstractTask):
    pass
