#!/usr/bin/python
# ex:set fileencoding=utf-8:
# flake8: noqa

from __future__ import unicode_literals

from django.test import LiveServerTestCase
from django.core.urlresolvers import reverse

from .models import Quotation, QuotationProduct
from ...testcase import ERPModuleTestCase


class QuotationModuleTests(ERPModuleTestCase):

    def test_urls_user(self):
        """
        """
        self.model = Quotation

        data = self.autotest_ajax_get('create')
        data = self.autotest_ajax_post('create', data={
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
        data = self.autotest_ajax_post('create', data={
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
        self.autotest_get('index', 200)

        obj = self.get_latest_object()

        self.autotest_get('detail', kwargs={'pk': obj.pk})
        data = self.autotest_ajax_get('update', kwargs={'pk': obj.pk})
        self.autotest_get('workflow', status_code=302, kwargs={'pk': obj.pk, 'transition': 'cancel'})
        self.autotest_get('delete', kwargs={'pk': obj.pk})
        self.autotest_post('delete', status_code=302, kwargs={'pk': obj.pk})

        obj = self.get_latest_object()

        self.autotest_get('workflow', status_code=302, kwargs={'pk': obj.pk, 'transition': 'send'})
        self.autotest_get('workflow', status_code=302, kwargs={'pk': obj.pk, 'transition': 'accept'})
        self.autotest_get('workflow', status_code=302, kwargs={'pk': obj.pk, 'transition': 'invoice'})

    def test_cleans(self):
        obj = Quotation()
        obj.clean()

        obj = QuotationProduct()
        obj.product_id = 1
        obj.clean()
        self.assertIsNotNone(obj.name, "name should be read from product")
        self.assertIsNotNone(obj.price, "price should be read from product")
