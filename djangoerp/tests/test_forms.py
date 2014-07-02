#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.test import LiveServerTestCase
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType

from ..utils import get_model_from_cfg

from ..testcase import ERPTestCase


class CoreTests(ERPTestCase):

    def test_forms(self):
        """
        """

        model = get_model_from_cfg("POSITION")
        namespace = model._erpmeta.url_namespace
        url = reverse(namespace + ':form-api')

        # don't accept get
        r = self.client.get(url)
        self.assertEqual(r.status_code, 403)

        # don't accept normal posts
        r = self.client.post(url, {})
        self.assertEqual(r.status_code, 403)

        # there is no search or update string attached
        r = self.client.post(url, {
            'form': 'project=&product=&employee=1&name=&date=01.01.2013&invoiceable=1&price=&amount=1.0&description=',
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(r.status_code, 404)

        r = self.client.post('%s?search' % url, {
            'form': 'project=&product=&employee=1&name=&date=01.01.2013&invoiceable=1&price=&amount=1.0&description=',
            'field': 'this_field_does_not_exist',
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(r.status_code, 404)

        r = self.client.post('%s?search' % url, {
            'form': 'project=&product=&employee=1&name=&date=01.01.2013&invoiceable=1&price=&amount=1.0&description=',
            'field': 'erp_product',
            'string': 'this_product_does_not_exist',
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.content, '[]')

        r = self.client.post('%s?search' % url, {
            'form': 'project=&product=&employee=1&name=&date=01.01.2013&invoiceable=1&price=&amount=1.0&description=',
            'field': 'erp_product',
            'string': 'Service',
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.content, '[{"pk": 1, "value": "Service"}]')

        r = self.client.post('%s?changed' % url, {
            'form': 'project=&product=1&employee=1&name=&date=01.01.2013&invoiceable=1&price=&amount=1.0&description=',
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.content, '[{"field": "erp_name", "value": "Service"}, {"field": "erp_price", "value": "69"}]')
