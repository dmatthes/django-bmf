# Django settings

from .test_settings import *

import os
from django.utils import six

gettext = lambda s: s
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

ADMINS = (
    ('Sebastian Braun', 'sebastian@elmnt.de'),
)

INTERNAL_IPS = ('127.0.0.1', '85.25.139.15')
ALLOWED_HOSTS = ["127.0.0.1"]

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Berlin'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'de'

TEST_PROJECT_APPS = (
    'djangobmf.contrib.accounting',
    'djangobmf.contrib.address',
    'djangobmf.contrib.customer',
#   'djangobmf.contrib.document',
    'djangobmf.contrib.employee',
    'djangobmf.contrib.invoice',
    'djangobmf.contrib.position',
    'djangobmf.contrib.product',
    'djangobmf.contrib.project',
    'djangobmf.contrib.quotation',
#   'djangobmf.contrib.shipment',
#   'djangobmf.contrib.stock',
    'djangobmf.contrib.task',
    'djangobmf.contrib.taxing',
    'djangobmf.contrib.team',
#   'djangobmf.contrib.timesheet',
    'djangobmf.currencies.EUR',
    'djangobmf.currencies.USD',
)
if six.PY2:
    TEST_PROJECT_APPS += (
        'djangobmf.reports.xhtml2pdf',
    )

INSTALLED_APPS += TEST_PROJECT_APPS

LANGUAGES = (
    (u'de', 'Deutsch'),
    (u'en', 'English'),
)

DEFAULT_FROM_EMAIL = "team@igelware.de"
SERVER_EMAIL = "noreply@igelware.de"

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake-439478'
  }
}

# BM ==============================================================================

BMF_DOCUMENT_ROOT = os.path.join(PROJECT_PATH, "bmf_documents")
BMF_DOCUMENT_URL = '/bmf_documents/'

# CELERY ==========================================================================

#import djcelery
#djcelery.setup_loader()
#CELERY_SEND_TASK_ERROR_EMAIL=True # ?????

# LOCAL SETTINGS ==================================================================

try:
    from local_settings import *
except ImportError:
    SECRET_KEY = 'just-a-dummy-key-overwrite-it-in:local_settings.py'
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': '%s/database.sqlite' % PROJECT_PATH,
            'USER': '',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
      }
    }
    DEBUG = True
    TEMPLATE_DEBUG = DEBUG
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    CELERY_ALWAYS_EAGER=True # deactivate celery

    INSTALLED_APPS += (
#       'django_extensions',
        'debug_toolbar',
    )
    MIDDLEWARE_CLASSES += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )
    DEBUG_TOOLBAR_CONFIG = {
        'JQUERY_URL': None,
    }

# LOGGING =========================================================================

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S",
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console':{
             'level': 'DEBUG',
             'filters': ['require_debug_true'],
             'class': 'logging.StreamHandler',
             'formatter': 'verbose',
         },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'djangobmf': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    }
}
