#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

SETTINGS = _('Settings')  # OLD
CR = _('Customer Relationship')  # OLD
HR = _('Human Resources')  # OLD
SALES = _('Sales')  # OLD
ACCOUNTING = _('Accounting')  # OLD
PURCHASES = _('Purchases')  # OLD
WAREHOUSE = _('Warehouse')  # OLD
KNOWLEDGE = _('Knowledge')  # OLD AND UNUSED
DOCUMENT = _('Documents')  # OLD
PROJECT = _('Projects')  # OLD


class BaseDashboard(object):
    pass


class BaseCategory(object):
    pass


# --- Predefined Dashboards ---------------------------------------------------


class ProjectManagement(BaseDashboard):
    name = _('Project Management')
    slug = "projects"


class DocumentManagement(BaseDashboard):
    name = _('Document Management')
    slug = "dms"


class Sales(BaseDashboard):
    name = _('Sales')
    slug = "sales"


class HumanResources(BaseDashboard):
    name = _('Human Resources')
    slug = "hr"


class CustomerRelationship(BaseDashboard):
    name = _('Customer Relationship')
    slug = "cr"


class Accounting(BaseDashboard):
    name = _('Accounting')
    slug = "accounting"


class Warehouse(BaseDashboard):
    name = _('Warehouse')
    slug = "warehouse"
