#!/usr/bin/python
# ex:set fileencoding=utf-8:
# flake8: noqa

from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType

from ..utils import get_model_from_cfg
from ..testcase import ERPModuleTestCase


class FormTests(ERPModuleTestCase):

    def test_forms(self):
        """
        """
        self.model = get_model_from_cfg("POSITION")

        # don't accept get
        self.autotest_get('form-api', status_code=403)

        # don't accept normal posts
        self.autotest_post('form-api', status_code=403)

        # there is no search or update string attached
        self.autotest_ajax_post('form-api', data={
            'form': 'project=&product=&employee=1&name=&date=01.01.2013&invoiceable=1&price=&amount=1.0&description=',
        }, status_code=404)

        self.autotest_ajax_post('form-api', parameter="search", data={
            'form': 'project=&product=&employee=1&name=&date=01.01.2013&invoiceable=1&price=&amount=1.0&description=',
            'field': 'this_field_does_not_exist',
        }, status_code=404)

        self.autotest_ajax_post('form-api', parameter="search", data={
            'form': 'project=&product=&employee=1&name=&date=01.01.2013&invoiceable=1&price=&amount=1.0&description=',
            'field': 'this_field_does_not_exist',
        }, status_code=404)

        data = self.autotest_ajax_post('form-api', parameter="search", data={
            'form': 'project=&product=&employee=1&name=&date=01.01.2013&invoiceable=1&price=&amount=1.0&description=',
            'field': 'erp_product',
            'string': 'this_product_does_not_exist',
        })
        self.assertEqual(data, [])

        data = self.autotest_ajax_post('form-api', parameter="search", data={
            'form': 'project=&product=&employee=1&name=&date=01.01.2013&invoiceable=1&price=&amount=1.0&description=',
            'field': 'erp_product',
            'string': 'Service',
        })
        self.assertEqual(data[0]["pk"], 1)
        self.assertEqual(data[0]["value"], "Service")

        data = self.autotest_ajax_post('form-api', parameter="changed", data={
            'form': 'project=&product=1&employee=1&name=&date=01.01.2013&invoiceable=1&price=&amount=1.0&description=',
        })
        self.assertEqual(data[0]["field"], "erp_name")
        self.assertEqual(data[0]["value"], "Service")
        self.assertEqual(data[1]["field"], "erp_price")
        self.assertEqual(data[1]["value"], "69")
