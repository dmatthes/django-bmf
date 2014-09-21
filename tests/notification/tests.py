#!/usr/bin/python
# ex:set fileencoding=utf-8:
# flake8: noqa

from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse

from djangobmf.notification.models import Notification
from djangobmf.signals import activity_create
from djangobmf.signals import activity_update
from djangobmf.utils.testcases import TestCase
from djangobmf.utils.testcases import ModuleMixin

from .models import TestNotification

from unittest import expectedFailure


class NotificationTests(ModuleMixin, TestCase):
    model = TestNotification

    def setUp(self):  # noqa
        super(NotificationTests, self).setUp()

        self.ct = ContentType.objects.get_for_model(TestNotification)

        self.user1 = self.create_user("user1", is_superuser=True)
        self.user2 = self.create_user("user2", is_superuser=True)

    def prepare_model_tests(self):
        fields = {
            'watch_ct': self.ct,
            'watch_id': None,
            'new_entry': True,
            'comment': True,
            'file': True,
            'changed': True,
            'workflow': True,
        }
        Notification.objects.create(user=self.user1, **fields)
        Notification.objects.create(user=self.user2, **fields)

        self.client_login("user2")

    def test_model_create(self):
        self.prepare_model_tests()
        object = TestNotification.objects.create(field="b")

        activity_create.send(sender=object.__class__, instance=object)

        self.assertEqual(Notification.objects.filter(watch_ct=self.ct, watch_id=object.pk).count(), 2, "Counting notification objects")

    @expectedFailure
    def test_model_comment(self):
        self.prepare_model_tests()
        self.assertEqual(1, 0, "not implemented")

    @expectedFailure
    def test_model_file(self):
        self.prepare_model_tests()
        self.assertEqual(1, 0, "not implemented")

    @expectedFailure
    def test_model_changed(self):
        self.prepare_model_tests()
        object = TestNotification.objects.create(field="b")

        object.field = "a"

        activity_update.send(sender=object.__class__, instance=object)

        self.assertEqual(Notification.objects.filter(watch_ct=self.ct, watch_id=object.pk).count(), 2, "Counting notification objects")

    @expectedFailure
    def test_model_workflow(self):
        self.prepare_model_tests()
        self.assertEqual(1, 0, "not implemented")

    def test_notification_views_index(self):
        """
        """
        self.client_login("user1")

        r = self.client.get(reverse('djangobmf:notification'))
        self.assertEqual(r.status_code, 200)

        r = self.client.get(reverse('djangobmf:notification', kwargs={"filter": "all"}))
        self.assertEqual(r.status_code, 200)

        r = self.client.get(reverse('djangobmf:notification', kwargs={"filter": "active"}))
        self.assertEqual(r.status_code, 200)

        self.assertEqual(Notification.objects.filter(user=self.user1).count(), 0)

        r = self.client.get(reverse('djangobmf:notification', kwargs={'ct': self.ct.pk, "filter": "all"}))
        self.assertEqual(r.status_code, 200)

        self.assertEqual(Notification.objects.filter(user=self.user1).count(), 1)

        r = self.client.get(reverse('djangobmf:notification', kwargs={'ct': self.ct.pk, "filter": "active"}))
        self.assertEqual(r.status_code, 200)

        r = self.client.get(reverse('djangobmf:notification', kwargs={'ct': self.ct.pk, "filter": "unread"}))
        self.assertEqual(r.status_code, 200)

    def test_notification_views_edit_root(self):
        self.client_login("user1")
        fields = {
            'user': self.user1,
            'watch_ct': self.ct,
            'watch_id': 0,
        }
        notification = Notification.objects.create(**fields)

        self.assertFalse(notification.new_entry)
        self.assertFalse(notification.comment)
        self.assertFalse(notification.file)
        self.assertFalse(notification.changed)
        self.assertFalse(notification.workflow)

        data = self.autotest_ajax_get(
            url=reverse('djangobmf:notification-update', kwargs={'pk': notification.pk}),
        )

        data = self.autotest_ajax_post(
            url=reverse('djangobmf:notification-update', kwargs={'pk': notification.pk}),
            data={
                'new_entry': True,
                'comment': True,
                'file': True,
                'changed': True,
                'workflow': True,
            }
        )
        notification = Notification.objects.get(**fields)

        self.assertTrue(notification.new_entry)
        self.assertTrue(notification.comment)
        self.assertTrue(notification.file)
        self.assertTrue(notification.changed)
        self.assertTrue(notification.workflow)

    def test_notification_views_edit_object(self):
        self.client_login("user1")
        object = TestNotification.objects.create(field="a")

        data = self.autotest_ajax_get(
            url=reverse('djangobmf:notification-create', kwargs={'ct': self.ct.pk, 'pk': object.pk}),
        )

        data = self.autotest_ajax_post(
            url=reverse('djangobmf:notification-create', kwargs={'ct': self.ct.pk, 'pk': object.pk}),
            data={
                'new_entry': True,
                'comment': True,
                'file': True,
                'changed': True,
                'workflow': True,
            }
        )
        notification = Notification.objects.get(**{
            'user': self.user1,
            'watch_ct': self.ct,
            'watch_id': object.pk,
        })
        self.assertFalse(notification.new_entry)
        self.assertTrue(notification.comment)
        self.assertTrue(notification.file)
        self.assertTrue(notification.changed)
        self.assertTrue(notification.workflow)

    def test_models(self):
        pass

    def test_tasks(self):
        pass
