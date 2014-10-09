#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from celery.task import task

from djangobmf.notification.tasks import djangobmf_user_watch as _djangobmf_user_watch


@task
def djangobmf_user_watch(*args, **kwargs):
    return _djangobmf_user_watch(*args, **kwargs)
