#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.conf import settings


def djangobmf_user_watch(activity):
    # from djangobmf.models import Notification
    from djangobmf.models import Watch

    from djangobmf.activity.models import ACTION_COMMENT
    from djangobmf.activity.models import ACTION_CREATED
    from djangobmf.activity.models import ACTION_UPDATED
    from djangobmf.activity.models import ACTION_WORKFLOW
    from djangobmf.activity.models import ACTION_FILE

    qs = Watch.objects.filter(watch_ct=activity.parent_ct, watch_id__in=[0, activity.parent_id])
    if activity.action == ACTION_COMMENT:
        qs = qs.filter(comment=True)
    elif activity.action == ACTION_UPDATED:
        qs = qs.filter(changed=True)
    elif activity.action == ACTION_WORKFLOW:
        qs = qs.filter(workflow=True)
    elif activity.action == ACTION_CREATED:
        qs = qs.filter(new_entry=True)
    elif activity.action == ACTION_FILE:
        qs = qs.filter(file=True)

    # LOOK ... maybe we can convert this into a one-liner :)
    user_list = []
    users = qs.values_list('user', flat=True)
    for i in users:
        if i not in user_list and i != activity.user_id:
            user_list.append(i)

    # Always add event to admin-user (pk=1) when in debug mode
    if settings.DEBUG:
        if 1 not in user_list:
            user_list.append(1)

    for user in user_list:
        # TODO check permissions!
        '''
        activity = Notification(
            user_id=user,
            activity=activity,
            obj_ct=activity.parent_ct,
            obj_id=activity.parent_id,
            created_by=activity.user,
        )
        activity.save()
        '''
        pass
