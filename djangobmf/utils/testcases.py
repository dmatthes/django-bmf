#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.apps import apps
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.urlresolvers import reverse
from django.test import LiveServerTestCase as DjangoLiveServerTestCase
from django.test import TransactionTestCase as DjangoTransactionTestCase
from django.test import TestCase as DjangoTestCase
from django.utils.translation import activate

from djangobmf.settings import CONTRIB_EMPLOYEE

import json


class BaseTestCase(object):
    def setUp(self):  # noqa
        from djangobmf import sites
        sites.autodiscover()
        activate('en')

        super(BaseTestCase, self).setUp()

    def create_user(self, username, is_staff=False, is_superuser=False,
                    is_active=True, permissions=None, create_employee=True):
        """
        This method is used to create users in test cases
        """
        user = get_user_model()
        username_field = user.USERNAME_FIELD

        fields = {
            'email': username + '@test.django-bmf.org',
            'is_staff': is_staff,
            'is_active': is_active,
            'is_superuser': is_superuser,
        }

        # Check for special case where email is used as username
        # if username_field != 'email':
        fields[username_field] = username

        user_obj = user(**fields)
        user_obj.set_password(getattr(user_obj, username_field))
        user_obj.save()

        # create employee object for user
        try:
            apps.get_model(CONTRIB_EMPLOYEE).objects.create(user=user_obj)
        except LookupError:
            pass

        if not is_superuser and permissions:
            for permission in permissions:
                user_obj.user_permissions.add(Permission.objects.get(codename=permission))

        return user_obj

    def client_login(self, username):
        # Check for special case where email is used as username
        # if get_user_model().USERNAME_FIELD == 'email':
        #     username += '@test.django-bmf.org'

        # update client
        self.client.login(username=username, password=username)


class ModuleMixin(object):
    model = None

    def get_latest_object(self):
        return self.model.objects.order_by('pk').last()

    def autotest_get(
            self, namespace=None, status_code=200, data=None, parameter=None,
            urlconf=None, args=None, kwargs=None, current_app=None, url=None):
        """
        tests the POST request of a view, returns the response
        """
        if not url:
            url = reverse(self.model._bmfmeta.url_namespace + ':' + namespace, urlconf, args, kwargs, current_app)
        if parameter:
            url += '?' + parameter
        r = self.client.get(url, data)
        self.assertEqual(r.status_code, status_code)
        return r

    def autotest_post(
            self, namespace=None, status_code=200, data=None, parameter=None,
            urlconf=None, args=None, kwargs=None, current_app=None, url=None):
        """
        tests the GET request of a view, returns the response
        """
        if not url:
            url = reverse(self.model._bmfmeta.url_namespace + ':' + namespace, urlconf, args, kwargs, current_app)
        if parameter:
            url += '?' + parameter
        r = self.client.post(url, data)
        self.assertEqual(r.status_code, status_code)
        return r

    def autotest_ajax_get(
            self, namespace=None, status_code=200, data=None, parameter=None,
            urlconf=None, args=None, kwargs=None, current_app=None, url=None):
        """
        tests the GET request of an ajax-view, returns the serialized data
        """
        if not url:
            url = reverse(self.model._bmfmeta.url_namespace + ':' + namespace, urlconf, args, kwargs, current_app)
        if parameter:
            url += '?' + parameter
        r = self.client.get(url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(r.status_code, status_code)
        if status_code == 200:
            return json.loads(r.content.decode())
        return r

    def autotest_ajax_post(
            self, namespace=None, status_code=200, data=None, parameter=None,
            urlconf=None, args=None, kwargs=None, current_app=None, url=None):
        """
        tests the POST request of an ajax-view, returns the serialized data
        """
        if not url:
            url = reverse(self.model._bmfmeta.url_namespace + ':' + namespace, urlconf, args, kwargs, current_app)
        if parameter:
            url += '?' + parameter
        r = self.client.post(url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(r.status_code, status_code)
        if status_code == 200:
            return json.loads(r.content.decode())
        return r


class TestCase(BaseTestCase, DjangoTestCase):
    pass


class TransactionTestCase(BaseTestCase, DjangoTransactionTestCase):
    pass


class LiveServerTestCase(BaseTestCase, DjangoLiveServerTestCase):
    pass


# OLD CODE BELOW THIS LINE -- DO NOT USE THIS


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
        from djangobmf import sites
        sites.autodiscover()
        self.client.login(username='admin', password='admin')
        activate('en')


class BMFModuleTestCase(ModuleMixin, BMFViewTestCase):
    pass


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
