#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.conf import settings
# from django.contrib.auth.models import Group
# from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class Dashboard(models.Model):
    user = models.ForeignKey(
        getattr(settings, 'AUTH_USER_MODEL', 'auth.User'), blank=True,
        null=True, related_name="+", on_delete=models.CASCADE,
    )
    # group = models.ForeignKey(Group, blank=True, null=True, related_name="+", on_delete=models.CASCADE)
    name = models.CharField(
        _("Name"),
        max_length=100, null=True, blank=False,
    )

    def __str__(self):
        if self.name:
            return self.name
        return "Root-Dashboard (%s)" % self.user

    def is_root(self):
        return not bool(self.name)

    class Meta:
        ordering = ('name', 'id',)
