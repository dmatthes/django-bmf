#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.test import LiveServerTestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from .models import Address
from ...testcase import ERPTestCase


class AddressTests(ERPTestCase):

    def test_urls_user(self):
        """
        """
        namespace = Address._erpmeta.url_namespace

        r = self.client.get(reverse(namespace + ':index'))
        self.assertEqual(r.status_code, 200)

        r = self.client.get(reverse(namespace + ':create'))
        self.assertEqual(r.status_code, 200)

        r = self.client.post(reverse(namespace + ':create'), {
            'customer': 1,
            'name': 'name',
            'street': 'street 12',
            'zip': '24342',
            'city': 'city',
            'state': 'state',
            'country': 'country',
            'is_active': '1',
        })
        self.assertEqual(r.status_code, 302)

        obj = Address.objects.order_by('pk').last()
        a = '%s' % obj # check if object name has any errors

        r = self.client.get(reverse(namespace + ':detail', None, None, {'pk': obj.pk}))
        self.assertEqual(r.status_code, 200)

        r = self.client.get(reverse(namespace + ':update', None, None, {'pk': obj.pk}))
        self.assertEqual(r.status_code, 200)

        r = self.client.get(reverse(namespace + ':delete', None, None, {'pk': obj.pk}))
        self.assertEqual(r.status_code, 200)

        r = self.client.post(reverse(namespace + ':delete', None, None, {'pk': obj.pk}))
        self.assertEqual(r.status_code, 302)

#lass PositionTests(LiveServerTestCase):
# fixtures=["djangoerp/fixtures_demo.json",]

# def test_urls_user(self):
#   """
#   """
#   self.client.login(username='admin',password='admin')
#   namespace = Position._erpmeta.url_namespace

#   r = self.client.get(reverse(namespace+':index'))
#   self.assertEqual(r.status_code, 301)

#   r = self.client.get(reverse(namespace+':table'))
#   self.assertEqual(r.status_code, 200)

#   r = self.client.get(reverse(namespace+':create'))
#   self.assertEqual(r.status_code, 200)

#   r = self.client.post(reverse(namespace+':create'),{'project':1, 'product':1})
#   self.assertEqual(r.status_code, 200)

#   r = self.client.post(reverse(namespace+':create'),{'project':2, 'product':1})
#   self.assertEqual(r.status_code, 200)

"""
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys

class MySeleniumTests(LiveServerTestCase):

  @classmethod
  def setUpClass(cls):
    cls.selenium = WebDriver()
    super(MySeleniumTests, cls).setUpClass()

  @classmethod
  def tearDownClass(cls):
    cls.selenium.quit()
    super(MySeleniumTests, cls).tearDownClass()

  def test_login(self):
    namespace = Address._erpmeta.url_namespace
    self.selenium.get('%s%s' % (self.live_server_url, '/en/'))

    username_field = self.selenium.find_element_by_name("username")
    username_field.send_keys('admin')
    password_field = self.selenium.find_element_by_name("password")
    password_field.send_keys('admin')
    password_field.send_keys(Keys.RETURN)

    self.selenium.get('%s%s' % (self.live_server_url, reverse(namespace+':index')))
    self.selenium.get('%s%s' % (self.live_server_url, reverse(namespace+':table')))
    self.selenium.get('%s%s' % (self.live_server_url, reverse(namespace+':create')))

"""
