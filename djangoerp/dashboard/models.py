#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.models import Group
from django.core.serializers.json import DjangoJSONEncoder
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

import json

class Dashboard(models.Model):
    user = models.ForeignKey(getattr(settings, 'AUTH_USER_MODEL', 'auth.User'), blank=True, null=True, related_name="+", on_delete=models.CASCADE)
   #group = models.ForeignKey(Group, blank=True, null=True, related_name="+", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=False)

    def __unicode__(self):
        if self.name:
            return self.name
        return "Root-Dashboard (%s)" % self.user

    def is_root(self):
        return not bool(self.name)

    class Meta:
        ordering = ('name', 'id',)


class View(models.Model):
    dashboard = models.ForeignKey(Dashboard, blank=False, null=True, related_name="views", on_delete=models.CASCADE)
    category = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=False)
    url = models.CharField(max_length=80, null=True, blank=False)
    kwargs = models.CharField(max_length=255, null=True, blank=True)
    search = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)

    def get_absolute_url(self):
        kwargs = json.loads(self.kwargs)
        url = reverse(self.url, kwargs=kwargs)
        if self.search:
            url += "?" + self.search
        return url
