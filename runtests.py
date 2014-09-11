#!/usr/bin/env python

import django
import re
import sys
import os
import tempfile

from django.conf import settings
from django.test.utils import get_runner

from djangobmf import contrib as bmfcontrib

from argparse import ArgumentParser
from coverage import coverage
from flake8.engine import get_style_guide

def main(modules, verbosity=2, failfast=False, contrib=None, nocontrib=False):

    print('*'*80)
    print('django ' + django.get_version())
    print('*'*80)

    # only write coverate into html and xml report
    # when all testcases are executed
    if len(modules) == 0 and not nocontrib and not contrib:
        coverreport = True
    else:
        coverreport = False

    # only test one contrib module
    if contrib:
        modules = ["djangobmf.contrib.%s" % contrib]

    # find tests in tests-directory
    if len(modules) == 0:
        path = "tests"
        for module in os.listdir(path):
            if os.path.isdir(os.path.join(path, module)):
                if module[0] == '_':
                    continue
                modules.append('tests.%s' % module)

        # find tests in contrib modules
        SKIPDIRS = []
        if not nocontrib:
            path = bmfcontrib.__path__[0]
            for module in os.listdir(path):
                if os.path.isdir(os.path.join(path, module)):
                    if module[0] == '_' or module in SKIPDIRS:
                        continue
                    modules.append('djangobmf.contrib.%s' % module)

    # flake8
    styleguide = get_style_guide(
        parse_argv=False,
        config_file="tox.ini",
        max_complexity=-1,
        jobs='1',
    )
    styleguide.options.report.start()
    styleguide.input_dir("djangobmf")
    styleguide.options.report.stop()
    if styleguide.options.report.get_count() > 0:
        sys.exit(True)

    # start coverage
    project_dir = os.path.dirname(__file__)
    if contrib:
        project_dir = os.path.join(os.path.dirname(__file__), "djangobmf", "contrib", contrib)
    else:
        project_dir = os.path.join(os.path.dirname(__file__), "djangobmf")

    cov_files = []

    for (path, dirs, files) in os.walk(project_dir):
        if os.path.basename(path) == 'tests' or os.path.basename(path) == "migrations":
            continue
        if nocontrib and not contrib and re.match(r'^djangobmf.contrib', path):
            continue
        cov_files.extend([os.path.join(path, file) for file in files if file.endswith('.py') and file != "tests.py"])
    cov = coverage()
    cov.erase()
    cov.start()

    # TODO

    TEMP_DIR = tempfile.mkdtemp(prefix='djangobmf_')

    settings.BMF_DOCUMENT_ROOT = TEMP_DIR
    settings.BMF_DOCUMENT_URL = '/documents/'

#   saveapps = settings.INSTALLED_APPS

    django.setup()

    failures = djangobmf_tests(verbosity, False, failfast, modules)

    cov.stop()

    if failures > 0:
        sys.exit(True)

    cov.report(cov_files)
    if coverreport:
        cov.xml_report(cov_files)
        cov.html_report(cov_files)

    sys.exit(False)


def djangobmf_tests(verbosity, interactive, failfast, test_labels):
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=verbosity, interactive=interactive, failfast=failfast)
    failures = test_runner.run_tests(test_labels)
    return failures


if __name__ == '__main__':
    parser = ArgumentParser(description="Run the django BMF test suite.")
    parser.add_argument('modules', nargs='*', metavar='module',
        help='Optional path(s) to test modules.')
    parser.add_argument(
        '-v', '--verbosity', default=1, type=int, choices=[0, 1, 2, 3],
        help='Verbosity level; 0=minimal output, 1=normal output, 2=all output'
    )
    parser.add_argument(
        '--failfast', action='store_true', dest='failfast', default=False,
        help='Stop running the test suite after first failed test.'
    )
    parser.add_argument(
        '--nocontrib', action='store_true', dest='nocontrib', default=False,
        help='Do not run testing on contrib modules.'
    )
    parser.add_argument(
        '--contrib',
        default=None,
        dest="contrib",
        help='Run tests only on the specified contrib module'
    )
#   parser.add_argument(
#       '--settings',
#       help='Python path to settings module, e.g. "myproject.settings". If '
#            'this isn\'t provided, either the DJANGO_SETTINGS_MODULE '
#            'environment variable or "test_sqlite" will be used.')
    options = parser.parse_args()
#   print (options)
#   options.modules = [os.path.normpath(labels) for labels in options.modules]

    if options.nocontrib:
        os.environ['DJANGO_SETTINGS_MODULE'] = "tests.test_sqlite"
    else:
        os.environ['DJANGO_SETTINGS_MODULE'] = "sandbox.settings"
#   if options.settings:
#       os.environ['DJANGO_SETTINGS_MODULE'] = options.settings
#   else:
#       if "DJANGO_SETTINGS_MODULE" not in os.environ:
#           os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.test_sqlite'

    main(
        options.modules,
        verbosity=options.verbosity,
        failfast=options.failfast,
        contrib=options.contrib,
        nocontrib=options.nocontrib,
    )

'''
import logging
import shutil
import subprocess
import warnings

import django
from django import contrib
from django.apps import apps
from django.conf import settings
from django.db import connection
from django.test import TransactionTestCase, TestCase
from django.utils.deprecation import RemovedInDjango19Warning, RemovedInDjango20Warning
from django.utils._os import upath
from django.utils import six

warnings.simplefilter("default", RemovedInDjango19Warning)
warnings.simplefilter("default", RemovedInDjango20Warning)

CONTRIB_MODULE_PATH = 'django.contrib'

TEST_TEMPLATE_DIR = 'templates'

CONTRIB_DIR = os.path.dirname(upath(contrib.__file__))
RUNTESTS_DIR = os.path.abspath(os.path.dirname(upath(__file__)))

TEMP_DIR = tempfile.mkdtemp(prefix='django_')
os.environ['DJANGO_TEST_TEMP_DIR'] = TEMP_DIR

SUBDIRS_TO_SKIP = [
    'data',
    'test_discovery_sample',
    'test_discovery_sample2',
    'test_runner_deprecation_app',
]

ALWAYS_INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admin.apps.SimpleAdminConfig',
    'django.contrib.staticfiles',
]

ALWAYS_MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)


def get_test_modules():
    modules = []
    discovery_paths = [
        (None, RUNTESTS_DIR),
        (CONTRIB_MODULE_PATH, CONTRIB_DIR)
    ]

    for modpath, dirpath in discovery_paths:
        for f in os.listdir(dirpath):
            if ('.' in f or
                    f.startswith('sql') or
                    os.path.basename(f) in SUBDIRS_TO_SKIP or
                    os.path.isfile(f) or
                    not os.path.exists(os.path.join(dirpath, f, '__init__.py'))):
                continue
            if not connection.vendor == 'postgresql' and f == 'postgres_tests':
                continue
            modules.append((modpath, f))
    return modules


def get_installed():
    return [app_config.name for app_config in apps.get_app_configs()]


def setup(verbosity, test_labels):

    state = {
        'INSTALLED_APPS': settings.INSTALLED_APPS,
        'ROOT_URLCONF': getattr(settings, "ROOT_URLCONF", ""),
        'TEMPLATE_DIRS': settings.TEMPLATE_DIRS,
        'LANGUAGE_CODE': settings.LANGUAGE_CODE,
        'STATIC_URL': settings.STATIC_URL,
        'STATIC_ROOT': settings.STATIC_ROOT,
        'MIDDLEWARE_CLASSES': settings.MIDDLEWARE_CLASSES,
    }

    # Redirect some settings for the duration of these tests.
    settings.INSTALLED_APPS = ALWAYS_INSTALLED_APPS
    settings.ROOT_URLCONF = 'urls'
    settings.STATIC_URL = '/static/'
    settings.STATIC_ROOT = os.path.join(TEMP_DIR, 'static')
    settings.TEMPLATE_DIRS = (os.path.join(RUNTESTS_DIR, TEST_TEMPLATE_DIR),)
    settings.LANGUAGE_CODE = 'en'
    settings.SITE_ID = 1
    settings.MIDDLEWARE_CLASSES = ALWAYS_MIDDLEWARE_CLASSES
    # Ensure the middleware classes are seen as overridden otherwise we get a compatibility warning.
    settings._explicit_settings.add('MIDDLEWARE_CLASSES')
    settings.MIGRATION_MODULES = {
        # these 'tests.migrations' modules don't actually exist, but this lets
        # us skip creating migrations for the test models.
        'auth': 'django.contrib.auth.tests.migrations',
        'contenttypes': 'django.contrib.contenttypes.tests.migrations',
    }

    if verbosity > 0:
        # Ensure any warnings captured to logging are piped through a verbose
        # logging handler.  If any -W options were passed explicitly on command
        # line, warnings are not captured, and this has no effect.
        logger = logging.getLogger('py.warnings')
        handler = logging.StreamHandler()
        logger.addHandler(handler)

    # Load all the ALWAYS_INSTALLED_APPS.
    django.setup()

    # Load all the test model apps.
    test_modules = get_test_modules()

    # Reduce given test labels to just the app module path
    test_labels_set = set()
    for label in test_labels:
        bits = label.split('.')
        if bits[:2] == ['django', 'contrib']:
            bits = bits[:3]
        else:
            bits = bits[:1]
        test_labels_set.add('.'.join(bits))

    installed_app_names = set(get_installed())
    for modpath, module_name in test_modules:
        if modpath:
            module_label = '.'.join([modpath, module_name])
        else:
            module_label = module_name
        # if the module (or an ancestor) was named on the command line, or
        # no modules were named (i.e., run all), import
        # this module and add it to INSTALLED_APPS.
        if not test_labels:
            module_found_in_labels = True
        else:
            module_found_in_labels = any(
                # exact match or ancestor match
                module_label == label or module_label.startswith(label + '.')
                for label in test_labels_set)

        if module_found_in_labels and module_label not in installed_app_names:
            if verbosity >= 2:
                print("Importing application %s" % module_name)
            settings.INSTALLED_APPS.append(module_label)

    apps.set_installed_apps(settings.INSTALLED_APPS)

    return state


def teardown(state):
    try:
        # Removing the temporary TEMP_DIR. Ensure we pass in unicode
        # so that it will successfully remove temp trees containing
        # non-ASCII filenames on Windows. (We're assuming the temp dir
        # name itself does not contain non-ASCII characters.)
        shutil.rmtree(six.text_type(TEMP_DIR))
    except OSError:
        print('Failed to remove temp directory: %s' % TEMP_DIR)

    # Restore the old settings.
    for key, value in state.items():
        setattr(settings, key, value)


def django_tests(verbosity, interactive, failfast, test_labels):
    state = setup(verbosity, test_labels)
    extra_tests = []

    # Run the test suite, including the extra validation tests.
    if not hasattr(settings, 'TEST_RUNNER'):
        settings.TEST_RUNNER = 'django.test.runner.DiscoverRunner'
    TestRunner = get_runner(settings)

    test_runner = TestRunner(
        verbosity=verbosity,
        interactive=interactive,
        failfast=failfast,
    )
    failures = test_runner.run_tests(
        test_labels or get_installed(),
        extra_tests=extra_tests
    )

    teardown(state)
    return failures
'''
