#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.views.generic import TemplateView


class WizardView(TemplateView):
    template_name = "djangoerp/wizard/index.html"
