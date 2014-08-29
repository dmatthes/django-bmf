#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals


from celery.task import task

from .bmf_tasks import account_balance as _account_balance


@task
def account_balance(*args, **kwargs):
    return _account_balance(*args, **kwargs)
