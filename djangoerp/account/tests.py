#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.test import LiveServerTestCase
from django.core.urlresolvers import reverse

class AccountTests(LiveServerTestCase):
    fixtures = ["djangoerp/fixtures_demousers.json", ]

    def test_views(self):
        """
        """
        r = self.client.get(reverse('djangoerp:login'), {})
        self.assertEqual(r.status_code, 200)

        r = self.client.post(reverse('djangoerp:login'), {
            'username': 'admin',
            'password': 'admin',
        })
        self.assertEqual(r.status_code, 302)

        r = self.client.get(reverse('djangoerp:login'), {})
        self.assertEqual(r.status_code, 200)

        r = self.client.post(reverse('djangoerp:login'), {
            'username': 'admin',
            'password': 'wrong_password',
        })
        self.assertEqual(r.status_code, 200)
