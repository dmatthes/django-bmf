#!/usr/bin/python
# ex:set fileencoding=utf-8:
# flake8: noqa

from __future__ import unicode_literals

from django.test import LiveServerTestCase
from django.core.urlresolvers import reverse

class AccountTests(LiveServerTestCase):
    fixtures = ["fixtures/users.json", ]

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

        r = self.client.get(reverse('djangobmf:login'), {})
        self.assertEqual(r.status_code, 200)

        r = self.client.post(reverse('djangobmf:login'), {
            'username': 'admin',
            'password': 'wrong_password',
        })
        self.assertEqual(r.status_code, 200)
