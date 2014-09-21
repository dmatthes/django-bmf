#!/usr/bin/python
# ex:set fileencoding=utf-8:
# flake8: noqa

from __future__ import unicode_literals

from django.core.urlresolvers import reverse

from djangobmf.testcases import TestCase


class NotificationTests(TestCase):
    def setUp(self):  # noqa
        super(NotificationTests, self).setUp()

        self.user1 = self.create_user("user1", is_superuser=False)
        self.user2 = self.create_user("user2", is_superuser=True)

    def test_notification(self):
        """
        """
        self.client_login("user1")

        r = self.client.get(reverse('djangobmf:notification'), {})
        self.assertEqual(r.status_code, 200)

        r = self.client.get(reverse('djangobmf:notification'), {'ct': 1})
        self.assertEqual(r.status_code, 200)

        r = self.client.get(reverse('djangobmf:notification'), {'filter': "all"})
        self.assertEqual(r.status_code, 200)

        r = self.client.get(reverse('djangobmf:notification'), {'ct': 1, 'filter': "all"})
        self.assertEqual(r.status_code, 200)
