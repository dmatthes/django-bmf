#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType

from .models import Goal
from .models import Task
from ...testcase import ERPTestCase
from ...testcase import ERPModuleTestCase

class TaskModuleTests(ERPModuleTestCase):

    def test_goal_views(self):
        self.model = Goal
        self.autotest_get('index', 200)
        data = self.autotest_ajax_get('create')
        data = self.autotest_ajax_post('create', data={'summary':'test'})

        obj = self.get_latest_object()
        a = '%s'%obj # check if object name has any errors

        self.autotest_get('detail', kwargs={'pk': obj.pk})
        data = self.autotest_ajax_get('update', kwargs={'pk': obj.pk})
        self.autotest_get('delete', status_code=403, kwargs={'pk': obj.pk})
        self.autotest_get('workflow', status_code=302, kwargs={'pk': obj.pk, 'transition': 'complete'})
        self.autotest_get('workflow', status_code=302, kwargs={'pk': obj.pk, 'transition': 'reopen'})
        self.autotest_get('workflow', status_code=302, kwargs={'pk': obj.pk, 'transition': 'complete'})
        self.autotest_get('delete', kwargs={'pk': obj.pk})
        self.autotest_post('delete', status_code=302, kwargs={'pk': obj.pk})

    def test_task_views(self):
        self.model = Task
        self.autotest_get('index')
        data = self.autotest_ajax_get('create')
        data = self.autotest_ajax_post('create', data={'summary':'test'})

        obj = self.get_latest_object()
        a = '%s'%obj # check if object name has any errors

        self.autotest_get('detail', kwargs={'pk': obj.pk})
        data = self.autotest_ajax_get('update', kwargs={'pk': obj.pk})
        self.autotest_get('delete', status_code=403, kwargs={'pk': obj.pk})
        self.autotest_get('workflow', status_code=302, kwargs={'pk': obj.pk, 'transition': 'finish'})
        self.autotest_get('delete', kwargs={'pk': obj.pk})
        self.autotest_post('delete', status_code=302, kwargs={'pk': obj.pk})

    def test_task_workflows(self):
        """
        """
        goal1 = Goal(summary="Goal1", project_id=1, billable=True)
        goal1.clean()
        goal1.save()

        goal2 = Goal(summary="Goal2", project_id=1, billable=True, referee_id=2)
        goal2.clean()
        goal2.save()

        goal2.erpget_customer()
        goal2.erpget_project()

        goal3 = Goal(summary="Goal3")
        goal3.clean()
        goal3.save()

        goal3.erpget_customer()

        task1 = Task(summary="Task1", goal=goal1)
        task1.clean()
        task1.save()

        task2 = Task(summary="Task2", goal=goal2)
        task2.clean()
        task2.save()

        task3 = Task(summary="Task3", project_id=1)
        task3.clean()
        task3.save()

        Project = task3.project._default_manager

        task3.get_goal_queryset(Goal.objects.all())

        task4 = Task(summary="Task4")
        task4.clean()
        task4.save()

        task5 = Task(summary="Task5", due_date='2014-01-01')
        task5.clean()
        task5.save()

        task5.get_project_queryset(Project.all())
        task5.get_goal_queryset(Goal.objects.all())

        task6 = Task(summary="Task6", due_date='2014-01-01', goal=goal1)
        task6.clean()
        task6.save()

        task6.get_project_queryset(Project.all())

        task7 = Task(summary="Task7", goal=goal1, seconds_on=1222, employee_id=1)
        task7.clean()
        task7.save()

        task8 = Task(summary="Task8", due_date='3014-01-01', goal=goal1)
        task8.clean()
        task8.save()

        namespace = Task._erpmeta.url_namespace

        r = self.client.get(reverse(namespace+':workflow', None, None, {'pk': task1.pk, 'transition': 'start'}))
        self.assertEqual(r.status_code, 302)

        r = self.client.get(reverse(namespace+':workflow', None, None, {'pk': task2.pk, 'transition': 'finish'}))
        self.assertEqual(r.status_code, 302)

        r = self.client.get(reverse(namespace+':workflow', None, None, {'pk': task2.pk, 'transition': 'finish'}))
        self.assertEqual(r.status_code, 200)

        r = self.client.get(reverse(namespace+':workflow', None, None, {'pk': task2.pk, 'transition': 'unreview'}))
        self.assertEqual(r.status_code, 302)

        r = self.client.get(reverse(namespace+':workflow', None, None, {'pk': task2.pk, 'transition': 'finish'}))
        self.assertEqual(r.status_code, 302)

        r = self.client.get(reverse(namespace+':workflow', None, None, {'pk': task4.pk, 'transition': 'hold'}))
        self.assertEqual(r.status_code, 302)

        r = self.client.get(reverse(namespace+':workflow', None, None, {'pk': task3.pk, 'transition': 'start'}))
        self.assertEqual(r.status_code, 302)

        r = self.client.get(reverse(namespace+':workflow', None, None, {'pk': task3.pk, 'transition': 'stop'}))
        self.assertEqual(r.status_code, 302)

        r = self.client.get(reverse(namespace+':workflow', None, None, {'pk': task3.pk, 'transition': 'finish'}))
        self.assertEqual(r.status_code, 302)

        r = self.client.get(reverse(namespace+':workflow', None, None, {'pk': task6.pk, 'transition': 'hold'}))
        self.assertEqual(r.status_code, 302)

        r = self.client.get(reverse(namespace+':workflow', None, None, {'pk': task7.pk, 'transition': 'cancel'}))
        self.assertEqual(r.status_code, 302)

        r = self.client.get(reverse(namespace+':workflow', None, None, {'pk': task7.pk, 'transition': 'reopen'}))
        self.assertEqual(r.status_code, 302)

        r = self.client.get(reverse(namespace+':workflow', None, None, {'pk': task7.pk, 'transition': 'finish'}))
        self.assertEqual(r.status_code, 302)

        namespace = Goal._erpmeta.url_namespace
        r = self.client.get(reverse(namespace + ':index'))
        self.assertEqual(r.status_code, 200)

        r = self.client.get(reverse(namespace+':detail', None, None, {'pk': goal1.pk}))
        self.assertEqual(r.status_code, 200)
     
        r = self.client.get(reverse(namespace+':detail', None, None, {'pk': goal2.pk}))
        self.assertEqual(r.status_code, 200)

        namespace = Task._erpmeta.url_namespace
        r = self.client.get(reverse(namespace + ':index'))
        self.assertEqual(r.status_code, 200)

 #      r = self.client.get(reverse(namespace + ':create'))
 #      self.assertEqual(r.status_code, 200)

        namespace = Goal._erpmeta.url_namespace

        r = self.client.get(reverse(namespace+':workflow', None, None, {'pk': goal1.pk, 'transition': 'complete'}))
        self.assertEqual(r.status_code, 200)
