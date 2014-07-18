#!/usr/bin/python
# ex:set fileencoding=utf-8:
# flake8: noqa

from __future__ import unicode_literals

from django.core.urlresolvers import reverse

from ..testcase import ERPTestCase

class DashboardTests(ERPTestCase):

    def test_dashboard(self):
        """
        """
        r = self.client.get(reverse('djangoerp:dashboard'))
        self.assertEqual(r.status_code, 200)

        r = self.client.get(reverse('djangoerp:dashboard_create'))
        self.assertEqual(r.status_code, 200)

 #      r = self.client.get(reverse('djangoerp:dashboard_update'))
 #      self.assertEqual(r.status_code, 200)

 #      r = self.client.get(reverse('djangoerp:dashboard_delete'))
 #      self.assertEqual(r.status_code, 200)

    def test_views(self):
        """
        """
