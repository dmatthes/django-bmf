#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.dispatch.dispatcher import Signal

activity_create = Signal(providing_args=['instance'])
activity_update = Signal(providing_args=['instance'])
activity_comment = Signal(providing_args=['instance'])
activity_addfile = Signal(providing_args=['instance', 'file'])
activity_workflow = Signal(providing_args=['instance'])
