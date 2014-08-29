#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import LiveServerTestCase
from django.test import TestCase
from django.utils.translation import activate

import json


class BMFViewTestCase(LiveServerTestCase):
    fixtures = [
        "fixtures/users.json",
        "fixtures/demodata.json",
        "fixtures/contrib_accounting.json",
        "fixtures/contrib_invoice.json",
        "fixtures/contrib_project.json",
        "fixtures/contrib_quotation.json",
        "fixtures/contrib_task.json",
        "fixtures/contrib_team.json",
    ]

    def setUp(self):  # noqa
        from . import sites
        sites.autodiscover()
        self.client.login(username='admin', password='admin')
        activate('en')


class BMFModuleTestCase(BMFViewTestCase):
    model = None

    def get_latest_object(self):
        return self.model.objects.order_by('pk').last()

    def autotest_get(
            self, namespace, status_code=200, data=None, parameter=None,
            urlconf=None, args=None, kwargs=None, current_app=None):
        """
        tests the POST request of a view, returns the response
        """
        url = reverse(self.model._bmfmeta.url_namespace + ':' + namespace, urlconf, args, kwargs, current_app)
        if parameter:
            url += '?' + parameter
        r = self.client.get(url, data)
        self.assertEqual(r.status_code, status_code)
        return r

    def autotest_post(
            self, namespace, status_code=200, data=None, parameter=None,
            urlconf=None, args=None, kwargs=None, current_app=None):
        """
        tests the GET request of a view, returns the response
        """
        url = reverse(self.model._bmfmeta.url_namespace + ':' + namespace, urlconf, args, kwargs, current_app)
        if parameter:
            url += '?' + parameter
        r = self.client.post(url, data)
        self.assertEqual(r.status_code, status_code)
        return r

    def autotest_ajax_get(
            self, namespace, status_code=200, data=None, parameter=None,
            urlconf=None, args=None, kwargs=None, current_app=None):
        """
        tests the GET request of an ajax-view, returns the serialized data
        """
        url = reverse(self.model._bmfmeta.url_namespace + ':' + namespace, urlconf, args, kwargs, current_app)
        if parameter:
            url += '?' + parameter
        r = self.client.get(url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(r.status_code, status_code)
        if status_code == 200:
            return json.loads(r.content.decode())
        return r

    def autotest_ajax_post(
            self, namespace, status_code=200, data=None, parameter=None,
            urlconf=None, args=None, kwargs=None, current_app=None):
        """
        tests the POST request of an ajax-view, returns the serialized data
        """
        url = reverse(self.model._bmfmeta.url_namespace + ':' + namespace, urlconf, args, kwargs, current_app)
        if parameter:
            url += '?' + parameter
        r = self.client.post(url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(r.status_code, status_code)
        if status_code == 200:
            return json.loads(r.content.decode())
        return r


class BMFWorkflowTestCase(TestCase):
    object = None

    def setUp(self):  # noqa
        self.user = get_user_model()(is_superuser=True)

    def workflow_build(self):
        wf = self.workflow_get()
        self.workflow = {}
        self.workflow_walk(wf._default_state_key)

    def workflow_walk(self, state):
        if state in self.workflow:
            return
        wf = self.workflow_get()
        wf._set_state(state)
        self.workflow[state] = {}

        for name, transition in wf._from_here():
            self.workflow[state][transition.target] = {
                'transition': name,
                'instance': self.object,
                'user': self.user,
                'manipulate_object': False,
            }
            self.workflow_walk(transition.target)

    def workflow_test(self, initial, final, instance, user=None, test_final=True):
        transition = self.workflow[initial][final]["transition"]
        wf = self.workflow_get()
        wf._set_state(initial)
        wf._call(transition, instance, user or self.user)
        if test_final:
            self.assertEqual(wf._current_state_key, final)

    def workflow_autotest(self):
        for i, data in self.workflow.items():
            for f, data in data.items():
                self.workflow_test(i, f, data["instance"], data["user"])

    def workflow_get(self):
        return self.object._bmfworkflow
