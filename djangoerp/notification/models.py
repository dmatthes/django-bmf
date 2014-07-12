#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Notification(models.Model):
    """
    Model which informs users about changes in the history
    """
    user = models.ForeignKey(getattr(settings, 'AUTH_USER_MODEL', 'auth.User'), blank=False, null=True, on_delete=models.CASCADE)
    activity = models.ForeignKey("djangoerp.Activity", blank=False, null=True, on_delete=models.CASCADE)
    obj_ct = models.ForeignKey(ContentType, related_name=False)
    obj_id = models.PositiveIntegerField()
    obj = GenericForeignKey('obj_ct', 'obj_id')
    unread = models.NullBooleanField(default=True)
    created = models.DateTimeField(_("Created"), auto_now_add=True, editable=False,)
    changed = models.DateTimeField(_("Changed"), auto_now=True, editable=False,)
    created_by = models.ForeignKey(getattr(settings, 'AUTH_USER_MODEL', 'auth.User'), blank=True, null=True, editable=False, related_name="+", on_delete=models.SET_NULL)

    class Meta:
        ordering = ('-created',)
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')
        get_latest_by = "modified"
        default_permissions=()

    def __str__(self):
        return self.name

