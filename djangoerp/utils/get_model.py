#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.apps import apps

from ..settings import BASE_MODULE

def get_model_from_name(str):
    path = str.split('.')
    return apps.get_model(path[0], path[1])

def get_model_from_cfg(str):
    return get_model_from_name(BASE_MODULE[str])
