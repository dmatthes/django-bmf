#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

import json

from ..signals import activity_create
from ..signals import activity_update
from ..signals import activity_addfile
from ..signals import activity_workflow

from ..settings import ACTIVITY_WORKFLOW
from ..settings import ACTIVITY_COMMENT
from ..settings import ACTIVITY_UPDATED
from ..settings import ACTIVITY_FILE
from ..settings import ACTIVITY_CREATED
from ..settings import ACTIVITY_UNKNOWN

# celery should be optional!
try:
    from ..tasks.djangobmf_user_watch import async as djangobmf_user_watch
except ImportError:
    from .tasks import djangobmf_user_watch

ACTION_COMMENT = 1
ACTION_CREATED = 2
ACTION_UPDATED = 3
ACTION_WORKFLOW = 4
ACTION_FILE = 5

ACTION_TYPES = (
    (ACTION_COMMENT, _("Comment")),
    (ACTION_CREATED, _("Created")),
    (ACTION_UPDATED, _("Updated")),
    (ACTION_WORKFLOW, _("Workflow")),
    (ACTION_FILE, _("File")),
)


@python_2_unicode_compatible
class Activity(models.Model):
    """
    Model which is accessed by en BMFModel with history
    """

    user = models.ForeignKey(
        getattr(settings, 'AUTH_USER_MODEL', 'auth.User'),
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    topic = models.CharField(_("Topic"), max_length=100, blank=True, null=True,)
    text = models.TextField(_("Text"), blank=True, null=True,)
    action = models.PositiveSmallIntegerField(
        _("Action"),
        blank=False,
        null=True,
        editable=False,
        default=ACTION_COMMENT,
        choices=ACTION_TYPES,
    )
    template = models.CharField(_("Template"), max_length=100, editable=False, blank=False, null=True)
    parent_id = models.PositiveIntegerField()
    parent_ct = models.ForeignKey(
        ContentType, related_name="bmf_history_parent", on_delete=models.CASCADE,
    )
    parent_object = GenericForeignKey('parent_ct', 'parent_id')

    modified = models.DateTimeField(_("Modified"), auto_now=True, editable=False,)

    class Meta:
        ordering = ('-modified',)
        verbose_name = _('History')
        verbose_name_plural = _('History')
        get_latest_by = "modified"

    def __str__(self):
        if self.topic:
            return self.topic
        else:
            return '%s %s' % (self.user, self.pk)

    def get_symbol(self):
        if self.action == ACTION_WORKFLOW:
            return ACTIVITY_WORKFLOW
        elif self.action == ACTION_COMMENT:
            return ACTIVITY_COMMENT
        elif self.action == ACTION_UPDATED:
            return ACTIVITY_UPDATED
        elif self.action == ACTION_FILE:
            return ACTIVITY_FILE
        elif self.action == ACTION_CREATED:
            return ACTIVITY_CREATED
        return ACTIVITY_UNKNOWN

    def get_template(self):
        if self.template:
            return self.template
        if self.action == ACTION_WORKFLOW:
            return "djangobmf/activities/workflow.html"
        elif self.action == ACTION_FILE:
            return "djangobmf/activities/file.html"
        elif self.action == ACTION_UPDATED:
            return "djangobmf/activities/updated.html"
        elif self.action == ACTION_CREATED:
            return "djangobmf/activities/created.html"
        return "djangobmf/activities/message.html"

    def get_text(self):
        if self.action == ACTION_WORKFLOW:
            data = json.loads(self.text)
            return {
                'new': self.parent_object._bmfmeta.workflow._states[data['new']],
                'old': self.parent_object._bmfmeta.workflow._states[data['old']],
            }
        elif self.action == ACTION_FILE:
            data = json.loads(self.text)
            return data
        return self.text

    def changes(self):
        if self.action == ACTION_UPDATED:
            data = json.loads(self.text)
            # update field names with the fields verbose name (and therefore its translation)
            for i in range(len(data)):
                for field in self.parent_ct.model_class()._meta.fields:
                    if field.name == data[i][0]:
                        data[i][0] = field.verbose_name
                        break
            return data
        return self.text


@receiver(activity_create)
def object_created(sender, instance, **kwargs):
    if instance._bmfmeta.has_history:
        history = Activity(
            user=instance.created_by,
            parent_ct=ContentType.objects.get_for_model(sender),
            parent_id=instance.pk,
            action=ACTION_CREATED,
        )
        history.save()


@receiver(activity_update)
def object_changed(sender, instance, **kwargs):
    if instance._bmfmeta.has_history and len(instance._bmfmeta.observed_fields) > 0:
        changes = []
        values = instance._get_observed_values()
        for key in instance._bmfmeta.observed_fields:
            try:
                if instance._bmfmeta.changelog[key] != values[key]:
                    changes.append((key, instance._bmfmeta.changelog[key], values[key]))
            except KeyError:
                pass
        if len(changes) > 0:
            history = Activity(
                user=instance.created_by,
                parent_ct=ContentType.objects.get_for_model(sender),
                parent_id=instance.pk,
                action=ACTION_UPDATED,
                text=json.dumps(changes, cls=DjangoJSONEncoder),
            )
            history.save()


@receiver(activity_workflow)
def new_state(sender, instance, **kwargs):
    if instance._bmfmeta.has_history:
        history = Activity(
            user=instance.created_by,
            parent_ct=ContentType.objects.get_for_model(sender),
            parent_id=instance.pk,
            action=ACTION_WORKFLOW,
            text=json.dumps({
                'old': instance._bmfworkflow._initial_state_key,
                'new': instance._bmfworkflow._current_state_key,
            }, cls=DjangoJSONEncoder),
        )
        history.save()


@receiver(activity_addfile)
def new_file(sender, instance, file, **kwargs):
    if instance._bmfmeta.has_history:
        history = Activity(
            user=instance.created_by,
            parent_ct=ContentType.objects.get_for_model(sender),
            parent_id=instance.pk,
            action=ACTION_FILE,
            text=json.dumps({
                'pk': file.pk,
                'size': file.size,
                'name': '%s' % file,
            }, cls=DjangoJSONEncoder),
        )
        history.save()


def activity_post_save(sender, instance, *args, **kwargs):
    djangobmf_user_watch(instance)
signals.post_save.connect(activity_post_save, sender=Activity)
