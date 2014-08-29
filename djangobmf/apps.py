#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.apps import AppConfig


class ERPConfig(AppConfig):
    name = 'djangoerp'
    label = 'djangoerp'
    verbose_name = "Django ERP"


class ContribTemplate(AppConfig):
    verbose_name = "Django ERP Contrib"
