#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .views import WizardView

urlpatterns = patterns(
    '',
    url(r'^$', WizardView.as_view(), name="wizard"),
)
