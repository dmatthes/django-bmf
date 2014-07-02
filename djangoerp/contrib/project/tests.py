#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.test import LiveServerTestCase
from django.core.urlresolvers import reverse

from .models import Project
from ...testcase import ERPTestCase


class ProjectTests(ERPTestCase):

    def test_urls_user(self):
        """
        """
        namespace = Project._erpmeta.url_namespace

        r = self.client.get(reverse(namespace + ':create'))
        self.assertEqual(r.status_code, 200)

        r = self.client.post(reverse(namespace + ':create'), {'customer': 1, 'employee': 1, 'name': 'Test'})
        self.assertEqual(r.status_code, 302)

        r = self.client.get(reverse(namespace + ':index'))
        self.assertEqual(r.status_code, 200)

        obj = Project.objects.order_by('pk').last()
        a = '%s' % obj # check if object name has any errors

        r = self.client.get(reverse(namespace + ':detail', None, None, {'pk': obj.pk}))
        self.assertEqual(r.status_code, 200)

        r = self.client.get(reverse(namespace + ':update', None, None, {'pk': obj.pk}))
        self.assertEqual(r.status_code, 200)

        r = self.client.get(reverse(namespace + ':delete', None, None, {'pk': obj.pk}))
        self.assertEqual(r.status_code, 200)

        r = self.client.post(reverse(namespace + ':delete', None, None, {'pk': obj.pk}))
        self.assertEqual(r.status_code, 302)
