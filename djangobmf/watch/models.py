#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Watch(models.Model):
    """
    Model which informs users about changes in the history
    """
    user = models.ForeignKey(getattr(settings, 'AUTH_USER_MODEL', 'auth.User'), blank=True, null=True)
    watch_ct = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    watch_id = models.PositiveIntegerField()
    watch_object = GenericForeignKey('watch_ct', 'watch_id')

    active = models.BooleanField(_("Active"), default=False, editable=False, db_index=True)

    new_entry = models.BooleanField(_("New entry"), default=False, db_index=True)
    comment = models.BooleanField(_("Comment written"), default=False, db_index=True)
    file = models.BooleanField(_("File added"), default=False, db_index=True)
    changed = models.BooleanField(_("Object changed"), default=False, db_index=True)
    workflow = models.BooleanField(_("Workflowstate changed"), default=False, db_index=True)

    modified = models.DateTimeField(_("Modified"), auto_now=True, editable=False,)

    class Meta:
        unique_together = (('user', 'watch_ct', 'watch_id'),)
        ordering = ('-modified',)
        verbose_name = _('Watched activity')
        verbose_name_plural = _('Watched activities')
        get_latest_by = "modified"
        default_permissions = ()

    def __str__(self):
        return '%s %s' % (self.user, self.watch_ct)

    def clean(self):
        if self.comment or self.file or self.changed or self.workflow:
            self.active = True
        else:
            self.active = False
