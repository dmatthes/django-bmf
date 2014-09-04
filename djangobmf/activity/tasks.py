#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.conf import settings
from django.utils.timezone import now


def djangobmf_user_watch(activity):

    from djangobmf.models import Notification

    from djangobmf.activity.models import ACTION_COMMENT
    from djangobmf.activity.models import ACTION_CREATED
    from djangobmf.activity.models import ACTION_UPDATED
    from djangobmf.activity.models import ACTION_WORKFLOW
    from djangobmf.activity.models import ACTION_FILE

    if activity.action == ACTION_CREATED:

        for watch in Notification.objects.filter(watch_ct=activity.parent_ct, watch_id=0).select_related('user'):
            # TODO: add ACL / Permissions lookups
            # cls = activity.parent_ct.model_class()
            # validated = activity.parent_ct.model_class().objects.get(activity.parent_id)
            validated = True
            if validated:
                watch.pk = None
                watch.unread = True
                watch.new_entry = False
                watch.watch_id = activity.parent_id
                watch.last_seen_object = activity.pk
                watch.triggered = True
                watch.save()
    else:
        qs = Notification.objects.filter(watch_ct=activity.parent_ct, watch_id=activity.parent_id)
        if activity.action == ACTION_COMMENT:
            qs = qs.filter(comment=True)
        if activity.action == ACTION_UPDATED:
            qs = qs.filter(changed=True)
        if activity.action == ACTION_WORKFLOW:
            qs = qs.filter(workflow=True)
        if activity.action == ACTION_FILE:
            qs = qs.filter(file=True)
        qs.filter(triggered=False).update(triggered=True, seen=False, modified=now())
