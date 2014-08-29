#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.apps import AppConfig


class BMFConfig(AppConfig):
    name = 'djangobmf'
    label = 'djangobmf'
    verbose_name = "Django BMF"


class ContribTemplate(AppConfig):
    verbose_name = "Django BMF Contrib"
