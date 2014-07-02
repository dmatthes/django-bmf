#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.test import LiveServerTestCase
from django.core.urlresolvers import reverse

from .models import Position
from ...testcase import ERPTestCase


class PositionTests(ERPTestCase):

    def test_urls_user(self):
        """
        """
        namespace = Position._erpmeta.url_namespace

        r = self.client.get(reverse(namespace + ':create'))
        self.assertEqual(r.status_code, 200)

        r = self.client.get(reverse(namespace + ':api'))
        self.assertEqual(r.status_code, 404)

        r = self.client.post(reverse(namespace + ':api'))
        self.assertEqual(r.status_code, 302)

        r = self.client.post(reverse(namespace + ':create'), {'project': 1, 'name': 'Service', 'price': '100', 'product': 1, 'date': '2012-01-01', 'amount': '2.0', 'employee': 1, 'invoiceable': 1})
        self.assertEqual(r.status_code, 302)
        r = self.client.post(reverse(namespace + ':create'), {'project': 2, 'name': 'Service', 'price': '100', 'product': 1, 'date': '2012-01-02', 'amount': '0.1', 'employee': 1, 'invoiceable': 1})
        self.assertEqual(r.status_code, 302)

        r = self.client.post(reverse(namespace + ':create'), {'project': 1, 'name': 'Service', 'price': '100', 'product': 1, 'date': '2012-01-01', 'amount': '1.0', 'employee': 2, 'invoiceable': 1})
        self.assertEqual(r.status_code, 302)
        r = self.client.post(reverse(namespace + ':create'), {'project': 2, 'name': 'Service', 'price': '100', 'product': 1, 'date': '2012-01-02', 'amount': '5.0', 'employee': 2, 'invoiceable': 1})
        self.assertEqual(r.status_code, 302)

        r = self.client.get(reverse(namespace + ':index'))
        self.assertEqual(r.status_code, 200)

        obj = Position.objects.order_by('pk').last()
        a = '%s' % obj # check if object name has any errors
        self.assertEqual(obj.has_invoice(), False)

        r = self.client.get(reverse(namespace + ':detail', None, None, {'pk': obj.pk}))
        self.assertEqual(r.status_code, 200)

        r = self.client.get(reverse(namespace + ':update', None, None, {'pk': obj.pk}))
        self.assertEqual(r.status_code, 200)

        r = self.client.get(reverse(namespace + ':delete', None, None, {'pk': obj.pk}))
        self.assertEqual(r.status_code, 200)

        r = self.client.post(reverse(namespace + ':delete', None, None, {'pk': obj.pk}))
        self.assertEqual(r.status_code, 302)

        obj = Position.objects.filter(invoice__isnull=True)
        data = {}
        pks = []
        for i in obj:
            data['pk.%s' % i.pk] = 1
            pks.append(i.pk)

 #      r = self.client.post(reverse(namespace + ':api'), data)
 #      self.assertEqual(r.status_code, 302)

 #      obj = Position.objects.filter(pk__in=pks)
 #      for i in obj:
 #          self.assertEqual(bool(i.invoice_id), True)

    def test_cleans(self):
        obj = Position()
        obj.product_id = 1
        obj.clean()
        self.assertIsNotNone(obj.name, "name should be read from product")
        self.assertIsNotNone(obj.price, "price should be read from product")
