#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from .models import Configuration

SETTING_KEY = "%s.%s"

class ERPConfig(object):
    def __init__(self, app_label, name, field):
        self.app_label = app_label
        self.name = name
        self.field = field

    @property
    def key(self):
        return SETTING_KEY % (self.app_label, self.name)

    @property
    def required(self):
        return self.field.required

    @property
    def changed(self):
        return self.field.initial != self.value

    @property
    def label(self):
        if self.field.label:
            return self.field.label
        return self.key

    @property
    def default(self):
        return self.field.initial

    @property
    def value(self):
        try:
            value = Configuration.objects.get_value(self.app_label, self.name)
        except Configuration.DoesNotExist:
            value = self.field.initial
        return value
