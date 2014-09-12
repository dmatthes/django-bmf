#!/usr/bin/python
# ex:set fileencoding=utf-8:
# flake8: noqa

from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

class AccountTests(TestCase):
# fixtures = ["fixtures/users.json", ]

    def setUp(self):  # noqa
        self.user = User(username="admin", is_staff=True, is_active=True, is_superuser=True)
        self.user.set_password("admin")
        self.user.save()

    def test_views(self):
        """
        """
        r = self.client.get(reverse('djangobmf:login'), {})
        self.assertEqual(r.status_code, 200)

        r = self.client.post(reverse('djangobmf:login'), {
            'username': 'admin',
            'password': 'admin',
        })
        self.assertEqual(r.status_code, 302)

        r = self.client.get(reverse('djangobmf:logout'), {})

        r = self.client.get(reverse('djangobmf:login'), {})
        self.assertEqual(r.status_code, 200)

        r = self.client.post(reverse('djangobmf:login'), {
            'username': 'admin',
            'password': 'wrong_password',
        })
        self.assertEqual(r.status_code, 200)
