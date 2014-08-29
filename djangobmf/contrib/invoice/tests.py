#!/usr/bin/python
# ex:set fileencoding=utf-8:
# flake8: noqa

from __future__ import unicode_literals

from django.test import LiveServerTestCase
from django.core.urlresolvers import reverse

from factory.django import DjangoModelFactory
from unittest import expectedFailure

from .models import Invoice
from ...testcase import BMFModuleTestCase
from ...testcase import BMFWorkflowTestCase


class InvoiceFactory(DjangoModelFactory):
    class Meta:
        model = Invoice
   #customer = 1
   #project = 1
   #date = '2014-01-01'
   #invoice_address = 1
   #shipping_address = 1
   #employee = 1
   #invoice_number = "TEST INVOICE"


class InvoiceModuleTests(BMFModuleTestCase):

    def test_urls_user(self):
        """
        """
        self.model = Invoice

        data = self.autotest_ajax_get('create')
       #data = self.autotest_ajax_post('create', data={
       #})
        data = self.autotest_get('index')


@expectedFailure
class InvoiceWorkflowTests(BMFWorkflowTestCase):
    pass

   #def test_invoice_workflow(self):
   #    self.object = InvoiceFactory()
   #    workflow = self.workflow_build()
   #    workflow = self.workflow_autotest()
