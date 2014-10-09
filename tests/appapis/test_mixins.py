#!/usr/bin/python
# ex:set fileencoding=utf-8:
# flake8: noqa

from __future__ import unicode_literals

from django.test import TestCase

from djangobmf.viewmixins import BaseMixin

class MixinTests(TestCase):

    def test_base_mixin(self):
        obj = BaseMixin()
        self.assertEqual(obj.get_permissions(), [])
        self.assertEqual(obj.get_permissions(['test']), ['test'])

        self.assertEqual(obj.check_permissions(), True)

# 50, 57, 60, 65-70, 81-97, 106-172, 179-195, 202-231, 240, 243, 246-248, 251, 254-259, 262-266, 275-287, 298-300, 309-312, 321-324, 333, 337-340, 349, 353-356, 365-379, 382-384, 387-411, 421-429, 432-435
