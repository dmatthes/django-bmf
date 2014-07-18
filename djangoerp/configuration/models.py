#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

import json

CONFIGURATION_CACHE = {}

class ConfigurationManager(models.Manager):
    def get_value(self, app, name):
        """
        Returns the current ``Configuration`` based on the app-label and
        the name of the setting. The ``Configuration`` object is cached the first
        time it's retrieved from the database.
        """

        try:
            value = CONFIGURATION_CACHE[app][name]
            return value
        except KeyError:
            value = json.loads(self.get(app_label=app, field_name=name).value)

        if app in CONFIGURATION_CACHE:
            CONFIGURATION_CACHE[app][name] = value
        else:
            CONFIGURATION_CACHE[app] = {name: value,}

        return value

    def clear_cache(self):
        """Clears the ``Configuration`` object cache."""
        global CONFIGURATION_CACHE
        CONFIGURATION_CACHE = {}

class Configuration(models.Model):
    """
    Model to store informations about settings
    """

    app_label = models.CharField(
        _("Application"), max_length=100, editable=False, null=True, blank=False,
    )
    field_name = models.CharField(
        _("Fieldname"), max_length=100, editable=False, null=True, blank=False,
    )
    value = models.TextField(_("Value"), null=True, blank=False)

    class Meta:
        verbose_name = _('Configuration')
        verbose_name_plural = _('Configurations')
        default_permissions = ('change',)

    objects = ConfigurationManager()

    def save(self, *args, **kwargs):
        super(Configuration, self).save(*args, **kwargs)
        # Cached information will likely be incorrect now.
        if self.app_label in CONFIGURATION_CACHE:
            if self.field_name in CONFIGURATION_CACHE[self.app_label]:
                del CONFIGURATION_CACHE[self.app_label][self.field_name]

    def delete(self):
        super(Configuration, self).delete()
        if self.app_label in CONFIGURATION_CACHE:
            if self.field_name in CONFIGURATION_CACHE[self.app_label]:
                del CONFIGURATION_CACHE[self.app_label][self.field_name]

    def __str__(self):
        return '%s.%s' % (self.app_label, self.field_name)
