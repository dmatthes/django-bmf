#!/usr/bin/python
# ex:set fileencoding=utf-8:
# flake8: noqa

from __future__ import unicode_literals

from django.core.urlresolvers import reverse

from djangobmf.testcase import BMFViewTestCase

class DashboardTests(BMFViewTestCase):

    def test_dashboard(self):
        """
        """
        r = self.client.get(reverse('djangobmf:dashboard'))
        self.assertEqual(r.status_code, 200)

        r = self.client.get(reverse('djangobmf:dashboard_create'))
        self.assertEqual(r.status_code, 200)

 #      r = self.client.get(reverse('djangobmf:dashboard_update'))
 #      self.assertEqual(r.status_code, 200)

 #      r = self.client.get(reverse('djangobmf:dashboard_delete'))
 #      self.assertEqual(r.status_code, 200)

    def test_views(self):
        """
        """
