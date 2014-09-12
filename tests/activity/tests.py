#!/usr/bin/python
# ex:set fileencoding=utf-8:
# flake8: noqa

from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType

from djangobmf.utils import get_model_from_cfg

from djangobmf.models import Activity
from djangobmf.testcase import BMFModuleTestCase


class CoreTests(BMFModuleTestCase):

    def test_history(self):
        """
        """
        self.model = get_model_from_cfg("PROJECT")
        data = self.autotest_ajax_post('create', data={
            'customer': 1,
            'name': "Testproject",
            'employee': 1,
        })
        self.assertNotEqual(data["object_pk"], 0)
        obj = self.get_latest_object()
        ct = ContentType.objects.get_for_model(self.model)

        self.assertEqual(obj.name, "Testproject")
        self.assertEqual(int(Activity.objects.filter(parent_ct=ct, parent_id=obj.pk).count()), 1)

        r = self.client.get(reverse('djangobmf:activity_comment_add', None, None, {'pk': obj.pk, 'ct': ct.pk}))
        self.assertEqual(r.status_code, 302)

        # this should create a new entry
        r = self.client.post(reverse('djangobmf:activity_comment_add', None, None, {'pk': obj.pk, 'ct': ct.pk}), {
            'topic': "Testtopic",
            'text': 'Testtext',
        })
        self.assertEqual(r.status_code, 302)

        # this should create a new entry
        r = self.client.post(reverse('djangobmf:activity_comment_add', None, None, {'pk': obj.pk, 'ct': ct.pk}), {
            'topic': "Testtopic",
        })
        self.assertEqual(r.status_code, 302)

        # this should create a new entry
        r = self.client.post(reverse('djangobmf:activity_comment_add', None, None, {'pk': obj.pk, 'ct': ct.pk}), {
            'text': 'Testtext',
        })
        self.assertEqual(r.status_code, 302)

        # this should NOT create a new entry
        r = self.client.post(reverse('djangobmf:activity_comment_add', None, None, {'pk': obj.pk, 'ct': ct.pk}), {})
        self.assertEqual(r.status_code, 302)

        # now, we should have 2 comments connected to our object
        self.assertEqual(int(Activity.objects.filter(parent_ct=ct, parent_id=obj.pk).count()), 4)

        # creation of a tax leads to the creation of a comment
        self.model = get_model_from_cfg("TAX")
        data = self.autotest_ajax_post('create', data={
            'name': "Testtax",
            'rate': 10,
            'account': 10,
        })
        self.assertNotEqual(data["object_pk"], 0)
        obj = self.get_latest_object()
        ct = ContentType.objects.get_for_model(self.model)

        # changing the rate of a tax creates a log entry
        data = self.autotest_ajax_post('update', kwargs={'pk': obj.pk}, data={
            'name': "Testtax",
            'rate': 20,
            'account': 10,
        })
        self.assertNotEqual(data["object_pk"], 0)
        obj = self.get_latest_object()

        self.assertEqual(obj.rate, 20)
        self.assertEqual(int(Activity.objects.filter(parent_ct=ct, parent_id=obj.pk).count()), 2)
