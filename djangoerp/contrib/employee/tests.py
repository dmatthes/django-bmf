#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from .models import Employee
from ...testcase import ERPModuleTestCase

class TaxTests(ERPModuleTestCase):

    def test_urls_user(self):
        """
        """
        self.model = Employee

        data = self.autotest_ajax_get('create')
        data = self.autotest_ajax_post('create', data={
            'name': 'test',
            'email': 'testing@django-erp.org',
        })
        self.assertNotEqual(data["object_pk"], 0)
        self.autotest_get('index', 200)

        obj = self.get_latest_object()
        a = '%s'%obj # check if object name has any errors

        self.autotest_get('detail', kwargs={'pk': obj.pk})
        data = self.autotest_ajax_get('update', kwargs={'pk': obj.pk})
        self.autotest_get('delete', kwargs={'pk': obj.pk})
        self.autotest_post('delete', status_code=302, kwargs={'pk': obj.pk})
