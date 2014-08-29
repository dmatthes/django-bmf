#!/usr/bin/python
# ex:set fileencoding=utf-8:
# flake8: noqa

from __future__ import unicode_literals

from django.test import TestCase

from django.core.exceptions import ImproperlyConfigured
from django.core.exceptions import ValidationError

from ..workflows import State, Transition, Workflow, DefaultWorkflow


class ClassTests(TestCase):
    def test_state(self):
        obj = State(b'name')
        self.assertEqual(obj.name, b"name")
        self.assertEqual(str(obj), "name")
        self.assertEqual(repr(obj), "<State: 'name'>")

    def test_transition(self):
        obj = Transition(b'name', 'from', 'to')
        self.assertEqual(obj.name, b"name")
        self.assertEqual(str(obj), "name")
        self.assertEqual(repr(obj), "<Transition: 'name'>")
        self.assertEqual(obj.sources, ["from", ])

        # may even add a object ... but why should you do it?
        obj = Transition('name', object, 'to')
        self.assertEqual(obj.sources, [object, ])

        obj = Transition('name', ['from1', 'from2'], 'to')
        self.assertEqual(obj.sources, ["from1", "from2", ])

        self.assertEqual(obj.affected_states(), ["from1", "from2", "to"])

    def test_workflow(self):
        self.assertEqual(str(DefaultWorkflow()), "default")
        self.assertRaises(ValidationError, DefaultWorkflow, 'does_not_exist')

        # catch validations =======================================================

        msg = "States-class no defined"
        with self.assertRaises(ImproperlyConfigured, msg=msg):
            class TestWF(Workflow):
                class Transitions:
                    pass

        msg = "Transitions-class no defined"
        with self.assertRaises(ImproperlyConfigured, msg=msg):
            class TestWF(Workflow):
                class States:
                    pass

        msg = "States-class is empty"
        with self.assertRaises(ImproperlyConfigured, msg=msg):
            class TestWF(Workflow):
                class States:
                    pass

                class Transitions:
                    pass

        msg = "No default State set"
        with self.assertRaises(ImproperlyConfigured, msg=msg):
            class TestWF(Workflow):
                class States:
                    test = State('Test', default=False)

                class Transitions:
                    pass

        msg = "Two default States set"
        with self.assertRaises(ImproperlyConfigured, msg=msg):
            class TestWF(Workflow):
                class States:
                    test1 = State('Test 1', default=True)
                    test2 = State('Test 2', default=True)

                class Transitions:
                    pass

        msg = "Transition-State is not valid"
        with self.assertRaises(ImproperlyConfigured, msg=msg):
            class TestWF(Workflow):
                class States:
                    test1 = State('Test 1', default=True)
                    test2 = State('Test 2')

                class Transitions:
                    trans1 = Transition('Transition 1', 'test1', 'test3')

        msg = "reserved name: instance"
        with self.assertRaises(ImproperlyConfigured, msg=msg):
            class TestWF(Workflow):
                class States:
                    test1 = State('Test 1', default=True)
                    test2 = State('Test 2')

                class Transitions:
                    instance = Transition('Transition 1', 'test1', 'test2')

        msg = "transition name starts with underscrore"
        with self.assertRaises(ImproperlyConfigured, msg=msg):
            class TestWF(Workflow):
                class States:
                    test1 = State('Test 1', default=True)
                    test2 = State('Test 2')

                class Transitions:
                    _test = Transition('Transition 1', 'test1', 'test2')

        msg = "reserved name: user"
        with self.assertRaises(ImproperlyConfigured, msg=msg):
            class TestWF(Workflow):
                class States:
                    test1 = State('Test 1', default=True)
                    test2 = State('Test 2')

                class Transitions:
                    user = Transition('Transition 1', 'test1', 'test2')

        # test API ================================================================

        # this is valid (jeah)
        class TestWF(Workflow):
            class States:
                test1 = State('Test 1', default=True)
                test2 = State('Test 2')
                test3 = State('Test 3')
                test4 = State('Test 4')
                test5 = State('Test 5')

            class Transitions:
                trans1 = Transition('Transition 1', 'test1', 'test2')
                trans2 = Transition('Transition 2', ['test1', 'test2'], 'test3')
                trans3 = Transition('Transition 3', ['test2', 'test3'], 'test4')
                trans4 = Transition('Transition 4', 'test4', 'test5')

            def trans2(self):
                return 'custom function called'

            def trans3(self):
                return self.trans2()

        WF = TestWF()
        self.assertTrue(hasattr(WF, 'trans1'), "Test 2")

        WF._set_state('test2')
        self.assertEqual(str(WF), "Test 2")
        self.assertEqual(WF._from_here(), [('trans2', WF._transitions['trans2']), ('trans3', WF._transitions['trans3'])])

        msg = "reserved name: instance"
        with self.assertRaises(ValidationError, msg=msg):
            WF._call('trans1', None, None)
        self.assertEqual(WF._call('trans2', None, None), "custom function called")
        self.assertEqual(WF._call('trans3', None, None), "custom function called")
        self.assertEqual(WF._call('trans4', None, None), None)


from django.test import LiveServerTestCase
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType

from ..utils import get_model_from_cfg
from ..testcase import BMFModuleTestCase


class ViewTests(BMFModuleTestCase):

    def test_views(self):
        """
        """

        self.model = get_model_from_cfg("QUOTATION")
        self.autotest_ajax_post('create', data={
            'project': 1,
            'customer': 1,
            'date': '2012-01-01',
            'employee': 1,
            'bmf-products-TOTAL_FORMS': 1,
            'bmf-products-INITIAL_FORMS': 0,
            'bmf-products-MAX_NUM_FORMS': 1,
            'bmf-products-0-product': 1,
            'bmf-products-0-amount': 1,
            'bmf-products-0-price': 100,
            'bmf-products-0-name': "Service",
        })

        model = get_model_from_cfg("QUOTATION")
        namespace = model._bmfmeta.url_namespace

        obj = self.model.objects.order_by('pk').last()

        # a quotation can't be deleted, if workflow state is not canceled
        r = self.client.get(reverse(namespace + ':delete', None, None, {'pk': obj.pk}))
        self.assertEqual(r.status_code, 403)
