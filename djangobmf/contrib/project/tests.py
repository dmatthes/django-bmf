#!/usr/bin/python
# ex:set fileencoding=utf-8:
# flake8: noqa

from __future__ import unicode_literals

from .models import Project
from ...testcase import BMFModuleTestCase

class ProjectTests(BMFModuleTestCase):

    def test_urls_user(self):
        """
        """
        self.model = Project

        data = self.autotest_ajax_get('create')
        data = self.autotest_ajax_post('create', data={
            'customer': 1,
            'employee': 1,
            'name': 'Test',
        })
        self.assertNotEqual(data["object_pk"], 0)
        self.autotest_get('index', 200)

        obj = self.get_latest_object()
        a = '%s'%obj # check if object name has any errors

        self.autotest_get('detail', kwargs={'pk': obj.pk})
        data = self.autotest_ajax_get('update', kwargs={'pk': obj.pk})
        self.autotest_get('delete', kwargs={'pk': obj.pk})
        self.autotest_post('delete', status_code=302, kwargs={'pk': obj.pk})
