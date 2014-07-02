#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.test import LiveServerTestCase
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType

from ..utils import get_model_from_cfg

from ..models import Report
from ..testcase import ERPTestCase


class CoreTests(ERPTestCase):

    def test_history_files(self):
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

        r = self.client.get(reverse('djangoerp:file_add', None, None, {'pk': obj.pk, 'ct': ct.pk}))
        self.assertEqual(r.status_code, 302)

        r = self.client.post(reverse('djangoerp:file_add', None, None, {'pk': obj.pk, 'ct': ct.pk}), {})
        self.assertEqual(r.status_code, 302)

        file = open('README.rst', 'r')
        r = self.client.post(reverse('djangoerp:file_add', None, None, {'pk': obj.pk, 'ct': ct.pk}), {
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
