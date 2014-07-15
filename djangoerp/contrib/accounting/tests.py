#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.test import LiveServerTestCase
from django.core.urlresolvers import reverse

import unittest

from .models import Account
from ...testcase import ERPModuleTestCase


class AccountModuleTests(ERPModuleTestCase):

    def test_get_urls(self):
        """
        """
        self.model = Account

        data = self.autotest_ajax_get('create')
        data = self.autotest_ajax_post('create', data={
            'number': "1",
            'name': "account 1",
            'type': 50,
        })
        self.autotest_get('index', 200)

        obj = self.get_latest_object()
        a = '%s'%obj # check if object name has any errors

        self.autotest_get('detail', kwargs={'pk': obj.pk})
        data = self.autotest_ajax_get('update', kwargs={'pk': obj.pk})
        self.autotest_get('delete', kwargs={'pk': obj.pk})
        self.autotest_post('delete', status_code=302, kwargs={'pk': obj.pk})
