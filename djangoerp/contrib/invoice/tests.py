#!/usr/bin/python
# ex:set fileencoding=utf-8:
# flake8: noqa

from __future__ import unicode_literals

from django.test import LiveServerTestCase
from django.core.urlresolvers import reverse

from .models import Invoice
from ...testcase import ERPModuleTestCase


class InvoiceModuleTests(ERPModuleTestCase):

    def test_urls_user(self):
        """
        """
        self.model = Invoice

        data = self.autotest_ajax_get('create')
       #data = self.autotest_ajax_post('create', data={
       #})
        data = self.autotest_get('index')
