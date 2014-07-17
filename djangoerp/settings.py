#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

"""
overwrites erp settings from django's settings
"""

from django.conf import settings
from django.core.files.storage import get_storage_class

__all__ = (
    'BASE_MODULE',
#   'FILE_SERVER',
    'DOCUMENT_ROOT',
    'DOCUMENT_URL',
    'STORAGE',
    'STORAGE_OPTIONS',
)

# === activity symbols ========================================================

ACTIVITY_WORKFLOW = "glyphicon-random"
ACTIVITY_COMMENT = "glyphicon-comment"
ACTIVITY_UPDATED = "glyphicon-pencil"
ACTIVITY_FILE = "glyphicon-paperclip"
ACTIVITY_CREATED = "glyphicon-file"
ACTIVITY_UNKNOWN = "glyphicon-question-sign"

# === modules =================================================================

erp_modules = getattr(settings, 'ERP_MODULES', {})
BASE_MODULE = {
    'ACCOUNT': 'djangoerp_accounting.Account',
    'ADDRESS': 'djangoerp_address.Address',
    'COMPANY': 'djangoerp_company.Company',
    'CUSTOMER': 'djangoerp_customer.Customer',
    'DOCUMENT': 'djangoerp_document.Document',
    'EMPLOYEE': 'djangoerp_employee.Employee',
    'GOAL': 'djangoerp_task.Goal',
    'INVOICE': 'djangoerp_invoice.Invoice',
    'TAX': 'djangoerp_taxing.Tax',
    'TEAM': 'djangoerp_team.Team',
    'POSITION': 'djangoerp_position.Position',
    'PRODUCT': 'djangoerp_product.Product',
    'PROJECT': 'djangoerp_project.Project',
    'QUOTATION': 'djangoerp_quotation.Quotation',
    'TIMESHEET': 'djangoerp_timesheet.Timesheet',
    'TRANSACTION': 'djangoerp_accounting.Transaction',
    'TRANSACTION_ITEM': 'djangoerp_accounting.TransactionItem',  # TODO: check if i am needed
}
BASE_MODULE.update(erp_modules)

# === storage =================================================================

erp_storage = getattr(settings, 'ERP_STORAGE', {})
CFG_STORAGE = {
    'ENGINE': 'django.core.files.storage.FileSystemStorage',
    'OPTIONS': {},
    'SERVER': 'djangoerp.backends.DefaultServer',
    'STATIC_PREFIX': 'static',
}
CFG_STORAGE.update(erp_storage)

if 'location' not in CFG_STORAGE['OPTIONS']:
    CFG_STORAGE['OPTIONS']['location'] = getattr(settings, 'ERP_DOCUMENT_ROOT', None)
if 'base_url' not in CFG_STORAGE['OPTIONS']:
    CFG_STORAGE['OPTIONS']['base_url'] = getattr(settings, 'ERP_DOCUMENT_URL', None)

if not CFG_STORAGE['OPTIONS']['location']:
    raise RuntimeError("django ERP module needs a setting ERP_DOCUMENTS_ROOT")
if not CFG_STORAGE['OPTIONS']['base_url']:
    raise RuntimeError("django ERP module needs a setting ERP_DOCUMENTS_URL")

DOCUMENT_ROOT = CFG_STORAGE['OPTIONS']['location']
DOCUMENT_URL = CFG_STORAGE['OPTIONS']['base_url']

STORAGE = get_storage_class(CFG_STORAGE['ENGINE'])
STORAGE_OPTIONS = CFG_STORAGE['OPTIONS']
STORAGE_STATIC_PREFIX = CFG_STORAGE['STATIC_PREFIX']
