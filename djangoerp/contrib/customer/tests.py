#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from .models import Customer
from ...testcase import ERPModuleTestCase

class CustomerTests(ERPModuleTestCase):

    def test_get_urls(self):
        """
        """
        self.model = Customer

        data = self.autotest_ajax_get('create', kwargs={"key": "company"})
        data = self.autotest_ajax_post('create', data={
            'name': "Company",
            'liability_account': 8,
            'asset_account': 13,
        }, kwargs={'key': 'company'})
        self.assertNotEqual(data["object_pk"], 0)

        data = self.autotest_ajax_get('create', kwargs={"key": "customer"})
        data = self.autotest_ajax_post('create', data={
            'name': "Customer",
            'liability_account': 8,
            'asset_account': 13,
        }, kwargs={'key': 'customer'})
        self.assertNotEqual(data["object_pk"], 0)

        self.autotest_get('index', 200)

        obj = self.get_latest_object()


        self.autotest_get('detail', kwargs={'pk': obj.pk})
        data = self.autotest_ajax_get('update', kwargs={'pk': obj.pk})
        self.autotest_get('delete', kwargs={'pk': obj.pk})
        obj.project.delete()
        self.autotest_post('delete', status_code=302, kwargs={'pk': obj.pk})
