#!/usr/bin/python
# ex:set fileencoding=utf-8:
# flake8: noqa

from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.core.urlresolvers import NoReverseMatch
from django.test import TestCase

from djangobmf.categories import BaseDashboard
from djangobmf.categories import BaseCategory
from djangobmf.workspace.models import Workspace

from djangobmf import sites

from .models import WorkspaceTest
from .views import WorkspaceTestView


class TestDashboard1(BaseDashboard):
    name = "Test1"
    slug = "test1"


class TestDashboard2(BaseDashboard):
    name = "Test2"
    slug = "test2"


class TestCategory1(BaseCategory):
    name = "Test1"
    slug = "test1"


class TestCategory2(BaseCategory):
    name = "Test2"
    slug = "test2"


class WorkspaceTests(TestCase):
    urls = 'tests.workspace.urls'

    def setUp(self):
        sites.autodiscover()
        Workspace.objects.all().delete()
        sites.site.register_dashboard(TestDashboard1)
        sites.site.register_category(TestDashboard1, TestCategory1)
        sites.site.register_view(WorkspaceTest, TestCategory1, WorkspaceTestView)

    def test_model_registration(self):
        # registration
        self.assertEqual(Workspace.objects.count(), 3)

    def test_model_types(self):
        dashboard, category, view = Workspace.objects.all()

        self.assertEqual(dashboard.type().title(), "Workspace")
        self.assertEqual(category.type().title(), "Category")
        self.assertEqual(view.type().title(), "View")

    def test_model_classes(self):
        dashboard, category, view = Workspace.objects.all()

        self.assertEqual(dashboard.module_cls, TestDashboard1)
        self.assertEqual(category.module_cls, TestCategory1)
        self.assertEqual(Workspace(module='Does.Not.Exist').module_cls, None)

    def test_model_clean_move(self):
        dashboard, category, view = Workspace.objects.all()

        msg = "change level while moving (view -> category)"
        with self.assertRaises(ValidationError, msg=msg):
            view.parent = dashboard
            view.clean()

        msg = "change level while moving (dashboard -> view)"
        with self.assertRaises(ValidationError, msg=msg):
            dashboard.parent = category
            dashboard.clean()

        msg = "change level while moving (category -> dashboard)"
        with self.assertRaises(ValidationError, msg=msg):
            category.parent = None
            category.clean()

    def test_model_clean_ct_dashboard(self):
        dashboard, category, view = Workspace.objects.all()

        dashboard.ct = view.ct
        dashboard.clean()
        self.assertEqual(dashboard.ct, None)

    def test_model_clean_ct_category(self):
        dashboard, category, view = Workspace.objects.all()

        category.ct = view.ct
        category.clean()
        self.assertEqual(category.ct, None)

    def test_model_clean_ct_view(self):
        dashboard, category, view = Workspace.objects.all()

        msg = "view with empty ct"
        with self.assertRaises(ValidationError, msg=msg):
            view.ct = None
            view.clean()

        msg = "append to view"
        with self.assertRaises(ValidationError, msg=msg):
            ws = Workspace(slug="testA", parent=view)
            ws.clean()

        msg = "no bmfmodule as ct"
        with self.assertRaises(ValidationError, msg=msg):
            view.ct = ContentType.objects.get_for_model(ContentType)
            view.clean()

    def test_model_misc(self):
        dashboard, category, view = Workspace.objects.all()
        self.assertEqual(category.parent, dashboard)

        # saves
        dashboard.slug = "db"
        dashboard.save()

        # str
        self.assertEqual('%s' % dashboard, TestDashboard1.name)
        self.assertEqual('%s' % Workspace(slug='testing'), 'testing')
        
        dashboard.get_absolute_url()

    def test_views(self):
        pass
