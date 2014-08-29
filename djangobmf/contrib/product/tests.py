#!/usr/bin/python
# ex:set fileencoding=utf-8:
# flake8: noqa

from __future__ import unicode_literals

from django.test import LiveServerTestCase
from django.core.urlresolvers import reverse

from .models import Product
from ...testcase import BMFModuleTestCase


class ProductTests(BMFModuleTestCase):

    def test_urls_user(self):
        """
        """
        self.model = Product

        data = self.autotest_ajax_get('create')
        # data = self.autotest_ajax_post('create', data={
        #     'number': "1",
        #     'name': "account 1",
        #     'type': 50,
        #})
        self.autotest_get('index', 200)

        obj = self.get_latest_object()
        a = '%s'%obj # check if object name has any errors

        self.autotest_get('detail', kwargs={'pk': obj.pk})
        data = self.autotest_ajax_get('update', kwargs={'pk': obj.pk})
        self.autotest_get('delete', kwargs={'pk': obj.pk})
        self.autotest_post('delete', status_code=302, kwargs={'pk': obj.pk})
