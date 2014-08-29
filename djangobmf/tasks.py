#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from celery.task import task

from djangoerp.activity.tasks import djangoerp_user_watch as _djangoerp_user_watch


@task
def djangoerp_user_watch(*args, **kwargs):
    return _djangoerp_user_watch(*args, **kwargs)
