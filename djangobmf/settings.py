#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

"""
overwrites bmf settings from django's settings
"""

from django.conf import settings
from django.core.files.storage import get_storage_class

__all__ = (
    'BASE_MODULE',
    # 'FILE_SERVER',
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

bmf_modules = getattr(settings, 'BMF_MODULES', {})
BASE_MODULE = {
    'ACCOUNT': 'djangobmf_accounting.Account',
    'ADDRESS': 'djangobmf_address.Address',
    'COMPANY': 'djangobmf_company.Company',
    'CUSTOMER': 'djangobmf_customer.Customer',
    'EMPLOYEE': 'djangobmf_employee.Employee',
    'GOAL': 'djangobmf_task.Goal',
    'INVOICE': 'djangobmf_invoice.Invoice',
    'TAX': 'djangobmf_taxing.Tax',
    'TASK': 'djangobmf_task.Task',
    'TEAM': 'djangobmf_team.Team',
    'POSITION': 'djangobmf_position.Position',
    'PRODUCT': 'djangobmf_product.Product',
    'PROJECT': 'djangobmf_project.Project',
    'QUOTATION': 'djangobmf_quotation.Quotation',
    'TIMESHEET': 'djangobmf_timesheet.Timesheet',
    'TRANSACTION': 'djangobmf_accounting.Transaction',
    'TRANSACTION_ITEM': 'djangobmf_accounting.TransactionItem',  # TODO: check if i am needed
}
BASE_MODULE.update(bmf_modules)

# === storage =================================================================

bmf_storage = getattr(settings, 'BMF_STORAGE', {})
CFG_STORAGE = {
    'ENGINE': 'django.core.files.storage.FileSystemStorage',
    'OPTIONS': {},
    'SERVER': 'djangobmf.backends.DefaultServer',
    'STATIC_PREFIX': 'static',
}
CFG_STORAGE.update(bmf_storage)

if 'location' not in CFG_STORAGE['OPTIONS']:
    CFG_STORAGE['OPTIONS']['location'] = getattr(settings, 'BMF_DOCUMENT_ROOT', None)
if 'base_url' not in CFG_STORAGE['OPTIONS']:
    CFG_STORAGE['OPTIONS']['base_url'] = getattr(settings, 'BMF_DOCUMENT_URL', None)

if not CFG_STORAGE['OPTIONS']['location']:
    raise RuntimeError("django BMF module needs a setting BMF_DOCUMENT_ROOT")
if not CFG_STORAGE['OPTIONS']['base_url']:
    raise RuntimeError("django BMF module needs a setting BMF_DOCUMENT_URL")

DOCUMENT_ROOT = CFG_STORAGE['OPTIONS']['location']
DOCUMENT_URL = CFG_STORAGE['OPTIONS']['base_url']

STORAGE = get_storage_class(CFG_STORAGE['ENGINE'])
STORAGE_OPTIONS = CFG_STORAGE['OPTIONS']
STORAGE_STATIC_PREFIX = CFG_STORAGE['STATIC_PREFIX']
