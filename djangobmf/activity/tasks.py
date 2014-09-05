#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

# from django.conf import settings
from django.utils.timezone import now

import logging
logger = logging.getLogger(__name__)


def djangobmf_user_watch(activity):

    from djangobmf.models import Notification

    from djangobmf.activity.models import ACTION_COMMENT
    from djangobmf.activity.models import ACTION_CREATED
    from djangobmf.activity.models import ACTION_UPDATED
    from djangobmf.activity.models import ACTION_WORKFLOW
    from djangobmf.activity.models import ACTION_FILE

    if activity.action == ACTION_CREATED:
        logger.debug("Notifications for new object: %s (%s)" % (activity.parent_ct, activity.parent_id))

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
            logger.debug("Notifications for comment: %s (%s)" % (activity.parent_ct, activity.parent_id))
            qs = qs.filter(comment=True)
        if activity.action == ACTION_UPDATED:
            logger.debug("Notifications for updated data: %s (%s)" % (activity.parent_ct, activity.parent_id))
            qs = qs.filter(changed=True)
        if activity.action == ACTION_WORKFLOW:
            logger.debug("Notifications for changed workflow: %s (%s)" % (activity.parent_ct, activity.parent_id))
            qs = qs.filter(workflow=True)
        if activity.action == ACTION_FILE:
            logger.debug("Notifications for appended file: %s (%s)" % (activity.parent_ct, activity.parent_id))
            qs = qs.filter(file=True)
        qs.update(triggered=True, unread=True, modified=now())
