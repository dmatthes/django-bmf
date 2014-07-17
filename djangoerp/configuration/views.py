#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django import forms
from django.core.urlresolvers import reverse
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from django.db import models
from django.views.generic import TemplateView
from django.views.generic import FormView

from ..viewmixins import ViewMixin
from ..models import Configuration
from ..sites import site, SETTING_KEY

import json


class ConfigurationView(ViewMixin, TemplateView):
    template_name = "djangoerp/configuration/index.html"

    def get_context_data(self, **kwargs):
        kwargs.update({
            'settings': site.settings,
        })
        return super(ConfigurationView, self).get_context_data(**kwargs)


class ConfigurationEdit(ViewMixin, FormView):
    template_name = "djangoerp/configuration/edit.html"

    def get_form_class(self):
        key = SETTING_KEY % (self.kwargs['app_label'], self.kwargs['name'])
        name = self.kwargs['name']
        class ConfigForm(forms.Form):
            """
            dynamic generated form with all settings
            """
            def __init__(self, *args, **kwargs):
                super(ConfigForm, self).__init__(*args, **kwargs)
                self.fields[name] = site.settings[key].field
        return ConfigForm

    def form_valid(self, form, *args, **kwargs):
        obj, created = Configuration.objects.get_or_create(app_label=self.kwargs['app_label'], field_name=self.kwargs['name'])
        value = form.cleaned_data[self.kwargs['name']]
        # data = {
        #     'type': None,
        #     'value': value,
        # }
        # if isinstance(value, models.Model):
        #     data['type'] = 'object'
        #     data['value'] = value.pk
        # obj.value = json.dumps(data, cls=DjangoJSONEncoder)
        if isinstance(value, models.Model):
            value = value.pk
        obj.value = json.dumps(value, cls=DjangoJSONEncoder)
        obj.save()
        return super(ConfigurationEdit, self).form_valid(form, *args, **kwargs)

    def get_success_url(self):
        return reverse('djangoerp:configuration')
