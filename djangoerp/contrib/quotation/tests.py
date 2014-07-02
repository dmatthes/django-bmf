#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.test import LiveServerTestCase
from django.core.urlresolvers import reverse

from .models import Quotation, QuotationProduct
from ...testcase import ERPTestCase


class QuotationTests(ERPTestCase):

    def test_urls_user(self):
        """
        """
        namespace = Quotation._erpmeta.url_namespace

        r = self.client.get(reverse(namespace + ':create'))
        self.assertEqual(r.status_code, 200)

        r = self.client.post(reverse(namespace + ':create'), {
            'project': 1,
            'customer': 1,
            'date': '2012-01-01',
            'employee': 1,
            'erp-products-TOTAL_FORMS': 1,
            'erp-products-INITIAL_FORMS': 0,
            'erp-products-MAX_NUM_FORMS': 1,
            'erp-products-0-product': 1,
            'erp-products-0-amount': 1,
            'erp-products-0-price': 100,
            'erp-products-0-name': "Service",
        })
        self.assertEqual(r.status_code, 302)
        r = self.client.post(reverse(namespace + ':create'), {
            'project': 2,
            'customer': 2,
            'date': '2012-01-01',
            'employee': 1,
            'erp-products-TOTAL_FORMS': 1,
            'erp-products-INITIAL_FORMS': 0,
            'erp-products-MAX_NUM_FORMS': 1,
            'erp-products-0-product': 1,
            'erp-products-0-amount': 10,
            'erp-products-0-price': 10,
            'erp-products-0-name': "Service",
        })
        self.assertEqual(r.status_code, 302)

        r = self.client.get(reverse(namespace + ':index'))
        self.assertEqual(r.status_code, 200)

        obj = Quotation.objects.order_by('pk').last()
        a = '%s' % obj # check if object name has any errors

        r = self.client.get(reverse(namespace + ':detail', None, None, {'pk': obj.pk}))
        self.assertEqual(r.status_code, 200)

        r = self.client.get(reverse(namespace + ':update', None, None, {'pk': obj.pk}))
        self.assertEqual(r.status_code, 200)

        r = self.client.get(reverse(namespace + ':workflow', None, None, {'pk': obj.pk, 'transition': 'cancel'}))
        self.assertEqual(r.status_code, 302)

        r = self.client.get(reverse(namespace + ':delete', None, None, {'pk': obj.pk}))
        self.assertEqual(r.status_code, 200)

        r = self.client.post(reverse(namespace + ':delete', None, None, {'pk': obj.pk}))
        self.assertEqual(r.status_code, 302)

        obj = Quotation.objects.order_by('pk').last()

        r = self.client.get(reverse(namespace + ':workflow', None, None, {'pk': obj.pk, 'transition': 'send'}))
        self.assertEqual(r.status_code, 302)

        r = self.client.get(reverse(namespace + ':workflow', None, None, {'pk': obj.pk, 'transition': 'accept'}))
        self.assertEqual(r.status_code, 302)

        r = self.client.get(reverse(namespace + ':workflow', None, None, {'pk': obj.pk, 'transition': 'invoice'}))
        self.assertEqual(r.status_code, 302)

    def test_cleans(self):
        obj = Quotation()
        obj.clean()

        obj = QuotationProduct()
        obj.product_id = 1
        obj.clean()
        self.assertIsNotNone(obj.name, "name should be read from product")
        self.assertIsNotNone(obj.price, "price should be read from product")
