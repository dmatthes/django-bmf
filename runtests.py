#!/usr/bin/env python

import django
import logging
import os
import re
import shutil
import sys
import tempfile
import warnings

from django.apps import apps
from django.conf import settings
from django.test.utils import get_runner
from django.utils import six

from djangobmf import contrib as bmfcontrib
from djangobmf import currencies as bmfcurrencies
from djangobmf import reports as bmfreports

from argparse import ArgumentParser
from coverage import coverage
from importlib import import_module
from flake8.engine import get_style_guide


def get_installed():
    return [app_config.name for app_config in apps.get_app_configs()]


def main(modules, verbosity=2, failfast=False, contrib=None, nocontrib=False):

    print('django ' + django.get_version())
    print('*'*80)

    # run flake8 first
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

    # apply test settings
    TEMP_DIR = tempfile.mkdtemp(prefix='djangobmf_')
    settings.BMF_DOCUMENT_ROOT = TEMP_DIR
    settings.BMF_DOCUMENT_URL = '/documents/'

    if verbosity > 0:
        # Ensure any warnings captured to logging are piped through a verbose
        # logging handler.
        logger = logging.getLogger('py.warnings')
        handler = logging.StreamHandler()
        logger.addHandler(handler)

    # Load all the app
    django.setup()

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

    # add currencies to INSTALLED_APPS
    path = bmfcurrencies.__path__[0]
    for module in os.listdir(path):
        if os.path.isdir(os.path.join(path, module)):
            if module[0] == '_':
                continue
            settings.INSTALLED_APPS += ('djangobmf.currencies.%s' % module, )

    # add reports to INSTALLED_APPS
    if six.PY2:
        path = bmfreports.__path__[0]
        for module in os.listdir(path):
            if os.path.isdir(os.path.join(path, module)):
                if module[0] == '_':
                    continue
                settings.INSTALLED_APPS += ('djangobmf.reports.%s' % module, )

    # update installed apps
    installed_app_names = set(get_installed())
    for module in modules:
        if module not in installed_app_names:
            if verbosity >= 2:
                print("Importing application %s" % module)
            settings.INSTALLED_APPS += (module, )
    apps.set_installed_apps(settings.INSTALLED_APPS)

    failures = djangobmf_tests(verbosity, False, failfast, modules)

    try:
        # Removing the temporary TEMP_DIR. Ensure we pass in unicode
        # so that it will successfully remove temp trees containing
        # non-ASCII filenames on Windows. (We're assuming the temp dir
        # name itself does not contain non-ASCII characters.)
        shutil.rmtree(six.text_type(TEMP_DIR))
    except OSError:
        print('Failed to remove temp directory: %s' % TEMP_DIR)

    sys.exit(bool(failures))


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
    parser.add_argument(
        '--settings',
        help='Python path to settings module, e.g. "myproject.settings". If '
             'this isn\'t provided, either the DJANGO_SETTINGS_MODULE '
             'environment variable or "test_sqlite" will be used.')
    options = parser.parse_args()

    if options.settings:
        os.environ['DJANGO_SETTINGS_MODULE'] = options.settings
    else:
        if "DJANGO_SETTINGS_MODULE" not in os.environ:
            os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.test_sqlite'

#   if options.nocontrib:
#       os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.test_sqlite'
#   else:
#       os.environ['DJANGO_SETTINGS_MODULE'] = 'sandbox.settings'

    main(
        options.modules,
        verbosity=options.verbosity,
        failfast=options.failfast,
        contrib=options.contrib,
        nocontrib=options.nocontrib,
    )
