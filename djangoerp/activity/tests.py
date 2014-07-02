#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.test import LiveServerTestCase
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType

from ..utils import get_model_from_cfg

from ..models import Activity
from ..testcase import ERPTestCase


class CoreTests(ERPTestCase):

    def test_history(self):
        """
        """
        model = get_model_from_cfg("PROJECT")
        namespace = model._erpmeta.url_namespace

        # creation of project leads to the creation of a comment
        r = self.client.post(reverse(namespace + ':create'), {
            'customer': 1,
            'name': "Testproject",
            'employee': 1,
        })
        self.assertEqual(r.status_code, 302)

        obj = model.objects.order_by('pk').last()
        ct = ContentType.objects.get_for_model(model)

        self.assertEqual(obj.name, "Testproject")
        self.assertEqual(int(Activity.objects.filter(parent_ct=ct, parent_id=obj.pk).count()), 1)

        r = self.client.get(reverse('djangoerp:activity_comment_add', None, None, {'pk': obj.pk, 'ct': ct.pk}))
        self.assertEqual(r.status_code, 302)

        # this should create a new entry
        r = self.client.post(reverse('djangoerp:activity_comment_add', None, None, {'pk': obj.pk, 'ct': ct.pk}), {
            'topic': "Testtopic",
            'text': 'Testtext',
        })
        self.assertEqual(r.status_code, 302)

        # this should create a new entry
        r = self.client.post(reverse('djangoerp:activity_comment_add', None, None, {'pk': obj.pk, 'ct': ct.pk}), {
            'topic': "Testtopic",
        })
        self.assertEqual(r.status_code, 302)

        # this should create a new entry
        r = self.client.post(reverse('djangoerp:activity_comment_add', None, None, {'pk': obj.pk, 'ct': ct.pk}), {
            'text': 'Testtext',
        })
        self.assertEqual(r.status_code, 302)

        # this should NOT create a new entry
        r = self.client.post(reverse('djangoerp:activity_comment_add', None, None, {'pk': obj.pk, 'ct': ct.pk}), {})
        self.assertEqual(r.status_code, 302)

        # now, we should have 2 comments connected to our object
        self.assertEqual(int(Activity.objects.filter(parent_ct=ct, parent_id=obj.pk).count()), 4)

        model = get_model_from_cfg("TAX")
        namespace = model._erpmeta.url_namespace

        # creation of a tax leads to the creation of a comment
        r = self.client.post(reverse(namespace + ':create'), {
            'name': "Testtax",
            'rate': 10,
            'account': 10,
        })
        self.assertEqual(r.status_code, 302)

        obj = model.objects.order_by('pk').last()
        ct = ContentType.objects.get_for_model(model)

        # changing the rate of a tax creates a log entry
        r = self.client.post(reverse(namespace + ':update', None, None, {'pk': obj.pk}), {
            'name': "Testtax",
            'rate': 20,
            'account': 10,
        })
        self.assertEqual(r.status_code, 302)

        obj = model.objects.order_by('pk').last()

        self.assertEqual(obj.rate, 20)
        self.assertEqual(int(Activity.objects.filter(parent_ct=ct, parent_id=obj.pk).count()), 2)
