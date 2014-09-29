#!/usr/bin/python
# ex:set fileencoding=utf-8:
# flake8: noqa

from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse

from djangobmf.models import Notification

from djangobmf.signals import activity_create
from djangobmf.signals import activity_update
from djangobmf.signals import activity_comment
from djangobmf.signals import activity_addfile
from djangobmf.signals import activity_workflow

from djangobmf.utils.testcases import TestCase
from djangobmf.utils.testcases import ModuleMixin

from .models import TestView

from unittest import expectedFailure


class NotificationTests(ModuleMixin, TestCase):
    model = TestView

    def activity_create_function(self, **kwargs):
        self.data_activity_create = kwargs

    def activity_update_function(self, **kwargs):
        self.data_activity_update = kwargs

    def activity_comment_function(self, **kwargs):
        self.data_activity_comment = kwargs

    def activity_addfile_function(self, **kwargs):
        self.data_activity_addfile = kwargs

    def activity_workflow_function(self, **kwargs):
        self.data_activity_workflow = kwargs


    def setUp(self):  # noqa
        super(NotificationTests, self).setUp()

        self.ct = ContentType.objects.get_for_model(TestView)
        self.user1 = self.create_user("user1", is_superuser=True)
        self.user2 = self.create_user("user2", is_superuser=True)

        self.data_activity_create = None
        self.data_activity_update = None
        self.data_activity_comment = None
        self.data_activity_addfile = None
        self.data_activity_workflow = None

        # Connect the listeners
        activity_create.connect(self.activity_create_function)
        activity_update.connect(self.activity_update_function)
        activity_comment.connect(self.activity_comment_function)
        activity_addfile.connect(self.activity_addfile_function)
        activity_workflow.connect(self.activity_workflow_function)

    def tearDown(self):
        # Disconnect the listeners
        activity_create.disconnect(self.activity_create_function)
        activity_update.disconnect(self.activity_update_function)
        activity_comment.disconnect(self.activity_comment_function)
        activity_addfile.disconnect(self.activity_addfile_function)
        activity_workflow.disconnect(self.activity_workflow_function)

    def prepare_signal_tests(self):
        fields = {
            'watch_ct': self.ct,
            'watch_id': 0,
            'new_entry': True,
            'comment': True,
            'file': True,
            'changed': True,
            'workflow': True,
        }
        Notification.objects.create(user=self.user1, **fields)
        Notification.objects.create(user=self.user2, **fields)
        self.client_login("user2")

    def test_signal_create(self):
        self.prepare_signal_tests()
        self.assertEqual(self.data_activity_create, None)

        object_pk = self.autotest_ajax_post('create', data={'field': 'a'})['object_pk']

        self.assertTrue(isinstance(self.data_activity_create["instance"], TestView))
        self.assertEqual(self.data_activity_create["instance"].created_by, self.user2)
        self.assertEqual(self.data_activity_create["instance"].modified_by, self.user2)

    @expectedFailure
    def test_signal_comment(self):
        # self.prepare_signal_tests()
        # object = TestView.objects.create(field="b")
        self.prepare_signal_tests()
        self.assertEqual(1, 0, "not implemented")

    @expectedFailure
    def test_signal_file(self):
        # self.prepare_signal_tests()
        # object = TestView.objects.create(field="b")
        self.assertEqual(1, 0, "not implemented")

    def test_signal_changed(self):
        self.prepare_signal_tests()
        object = TestView.objects.create(
            field="b",
            created_by=self.user1,
            modified_by=self.user1,
        )
        self.assertEqual(self.data_activity_update, None)

        self.autotest_ajax_post('update', kwargs={'pk': object.pk}, data={'field': 'a'})

        self.assertTrue(isinstance(self.data_activity_update["instance"], TestView))

        self.assertEqual(self.data_activity_update["instance"].created_by, self.user1)
        self.assertEqual(self.data_activity_update["instance"].modified_by, self.user2)

    @expectedFailure
    def test_signal_workflow(self):
        # self.prepare_signal_tests()
        # object = TestView.objects.create(field="b")
        self.assertEqual(1, 0, "not implemented")
