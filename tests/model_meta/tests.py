#!/usr/bin/python
# ex:set fileencoding=utf-8:
# flake8: noqa

from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, modify_settings

class BlubTests(TestCase):

    def test_views(self):
        """
        """
#       print( Category.objects.all() )
        self.assertEqual(1, 1)
