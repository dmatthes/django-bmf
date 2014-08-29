#!/usr/bin/python
# ex:set fileencoding=utf-8:
# flake8: noqa

from __future__ import unicode_literals

from django.test import LiveServerTestCase
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType

from ..utils import get_model_from_cfg

from ..models import Report
from ..testcase import BMFModuleTestCase


class CoreTests(BMFModuleTestCase):

    def test_history_files(self):
        """
        """

        self.model = get_model_from_cfg("PROJECT")
        self.autotest_ajax_post('create', data={
            'customer': 1,
            'name': "Testproject",
            'employee': 1,
        })

        model = get_model_from_cfg("PROJECT")
        namespace = model._bmfmeta.url_namespace

        obj = model.objects.order_by('pk').last()
        ct = ContentType.objects.get_for_model(model)

        r = self.client.get(reverse('djangobmf:file_add', None, None, {'pk': obj.pk, 'ct': ct.pk}))
        self.assertEqual(r.status_code, 302)

        r = self.client.post(reverse('djangobmf:file_add', None, None, {'pk': obj.pk, 'ct': ct.pk}), {})
        self.assertEqual(r.status_code, 302)

        file = open('README.rst', 'rb')
        r = self.client.post(reverse('djangobmf:file_add', None, None, {'pk': obj.pk, 'ct': ct.pk}), {
            'file': file,
        })
        self.assertEqual(r.status_code, 302)
        file.close()

        # now, we should have one file connected to our object
        model = get_model_from_cfg("DOCUMENT")
        query = model.objects.filter(content_type=ct, content_id=obj.pk)
        self.assertEqual(int(query.count()), 1)
        # cleanup
        for obj in query:
            obj.file.delete()
