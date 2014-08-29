#!/usr/bin/python
# ex:set fileencoding=utf-8:
# flake8: noqa

from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType

from ..utils import get_model_from_cfg
from ..testcase import BMFViewTestCase

class WatchTests(BMFViewTestCase):

    def test_watch(self):
        """
        """
        model = get_model_from_cfg("PROJECT")
        ct = ContentType.objects.get_for_model(model)

        r = self.client.get(reverse('djangobmf:watch'))
        self.assertEqual(r.status_code, 200)

        r = self.client.get(reverse('djangobmf:watch', kwargs={'ct': 1}))
        self.assertEqual(r.status_code, 404)

        r = self.client.get(reverse('djangobmf:watch', kwargs={'ct': ct.pk}))
        self.assertEqual(r.status_code, 200)

 #      r = self.client.get(reverse('djangobmf:watch_edit', kwargs={'ct': ct.pk, 'pk': 0}))
 #      self.assertEqual(r.status_code, 200)

 #      r = self.client.get(reverse('djangobmf:watch_edit', kwargs={'ct': ct.pk, 'pk': 1}))
 #      self.assertEqual(r.status_code, 200)

