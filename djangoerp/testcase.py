#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.test import LiveServerTestCase

import json


class ERPTestCase(LiveServerTestCase):
    fixtures = [
        "djangoerp/fixtures_demousers.json",
        "djangoerp/fixtures_demodata.json",
    ]

    def setUp(self):
        from . import sites
        sites.autodiscover()
        self.client.login(username='admin', password='admin')


class ERPModuleTestCase(ERPTestCase):
    model = None

    def get_latest_object(self):
        return self.model.objects.order_by('pk').last()

    def autotest_get(self, namespace, status_code=200, data=None, urlconf=None, args=None, kwargs=None, current_app=None):
        """
        tests the POST request of a view, returns the response
        """
        url = reverse(self.model._erpmeta.url_namespace + ':' + namespace, urlconf, args, kwargs, current_app)
        r = self.client.get(url, data)
        self.assertEqual(r.status_code, status_code)
        return r

    def autotest_post(self, namespace, status_code=200, data=None, urlconf=None, args=None, kwargs=None, current_app=None):
        """
        tests the GET request of a view, returns the response
        """
        url = reverse(self.model._erpmeta.url_namespace + ':' + namespace, urlconf, args, kwargs, current_app)
        r = self.client.post(url, data)
        self.assertEqual(r.status_code, status_code)
        return r

    def autotest_ajax_get(self, namespace, data=None, urlconf=None, args=None, kwargs=None, current_app=None):
        """
        tests the GET request of an ajax-view, returns the serialized data
        """
        url = reverse(self.model._erpmeta.url_namespace + ':' + namespace, urlconf, args, kwargs, current_app)
        r = self.client.get(url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(r.status_code, 200)
        return json.loads(r.content)

    def autotest_ajax_post(self, namespace, data=None, urlconf=None, args=None, kwargs=None, current_app=None):
        """
        tests the POST request of an ajax-view, returns the serialized data
        """
        url = reverse(self.model._erpmeta.url_namespace + ':' + namespace, urlconf, args, kwargs, current_app)
        r = self.client.post(url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(r.status_code, 200)
        return json.loads(r.content)
