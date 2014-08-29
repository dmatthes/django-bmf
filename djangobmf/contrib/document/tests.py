#!/usr/bin/python
# ex:set fileencoding=utf-8:
# flake8: noqa

from __future__ import unicode_literals

from .models import Document
from ...testcase import BMFModuleTestCase


class DocumentTests(BMFModuleTestCase):

    def test_urls_user(self):
        """
        """
        self.model = Document
        self.autotest_get('index', 200)

#   r = self.client.get(reverse(namespace+':create'))
#   self.assertEqual(r.status_code, 200)

#   r = self.client.post(reverse(namespace+':create'),{'name':1, 'account':3, 'rate':'10', 'is_active': '1'})
#   self.assertEqual(r.status_code, 302)

#   obj = Customer.objects.order_by('pk').last()
#   a = '%s'%obj # check if object name has any errors

#   r = self.client.get(reverse(namespace+':detail', None, None, {'pk': obj.pk}))
#   self.assertEqual(r.status_code, 200)

#   r = self.client.get(reverse(namespace+':update', None, None, {'pk': obj.pk}))
#   self.assertEqual(r.status_code, 200)

#   r = self.client.get(reverse(namespace+':delete', None, None, {'pk': obj.pk}))
#   self.assertEqual(r.status_code, 200)

#   r = self.client.post(reverse(namespace+':delete', None, None, {'pk': obj.pk}))
#   self.assertEqual(r.status_code, 302)
