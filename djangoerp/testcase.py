#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.test import LiveServerTestCase


class ERPTestCase(LiveServerTestCase):
    fixtures = [
        "djangoerp/fixtures_demousers.json",
        "djangoerp/fixtures_demodata.json",
    ]

    def setUp(self):
        from . import sites
        sites.autodiscover()
        self.client.login(username='admin', password='admin')
