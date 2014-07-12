#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.test import LiveServerTestCase
from django.core.urlresolvers import reverse

import unittest

from .models import Account
from ...testcase import ERPTestCase


class AccountTests(ERPTestCase):

    def test_get_urls(self):
        """
        """
        namespace = Account._erpmeta.url_namespace

        r = self.client.get(reverse(namespace + ':index'))
        self.assertEqual(r.status_code, 200)

        r = self.client.get(reverse(namespace + ':create'))
        self.assertEqual(r.status_code, 200)

        obj = Account.objects.order_by('pk').last()
        a = '%s' % obj # check if object name has any errors

        r = self.client.get(reverse(namespace + ':detail', None, None, {'pk': obj.pk}))
        self.assertEqual(r.status_code, 200)

        r = self.client.get(reverse(namespace + ':update', None, None, {'pk': obj.pk}))
        self.assertEqual(r.status_code, 200)

        r = self.client.get(reverse(namespace + ':delete', None, None, {'pk': obj.pk}))
        self.assertEqual(r.status_code, 200)

    @unittest.expectedFailure
    def test_post_urls(self):
        """
        """
        namespace = Account._erpmeta.url_namespace

        r = self.client.post(reverse(namespace+':create'),{'name':1, 'account':3, 'rate':'10', 'is_active': '1'})
        self.assertEqual(r.status_code, 302)

        obj = Account.objects.order_by('pk').last()
        a = '%s' % obj # check if object name has any errors

        r = self.client.post(reverse(namespace + ':delete', None, None, {'pk': obj.pk}))
        self.assertEqual(r.status_code, 302)
