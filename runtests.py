#!/usr/bin/env python

import django
import os
import re
import shutil
import sys
import tempfile

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

def main(modules, verbosity=2, failfast=False, contrib=None, nocontrib=False):

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

    TEMP_DIR = tempfile.mkdtemp(prefix='djangobmf_')
    settings.BMF_DOCUMENT_ROOT = TEMP_DIR
    settings.BMF_DOCUMENT_URL = '/documents/'

#   # add currencies to INSTALLED_APPS
#   path = bmfcurrencies.__path__[0]
#   for module in os.listdir(path):
#       if os.path.isdir(os.path.join(path, module)):
#           if module[0] == '_':
#               continue
#           print(module)
#           settings.INSTALLED_APPS += ('djangobmf.currencies.%s' % module, )

#   # add reports to INSTALLED_APPS
#   if six.PY2:
#       path = bmfreports.__path__[0]
#       for module in os.listdir(path):
#           if os.path.isdir(os.path.join(path, module)):
#               if module[0] == '_':
#                   continue
#               print(module)
#               settings.INSTALLED_APPS += ('djangobmf.reports.%s' % module, )


#   # add modules to settings.INSTALLED_APPS
#   for module_name in modules:
#       # TODO this does not support the path on the filesystem or to a specific testcase
#       # maybe we could implement this somewhere after the tests are discovered and
#       # update the installed apps after django.setup() is called
##      if re.match(r'^tests.[a-z_]+$', module_name) or re.match(r'^djangobmf.contrib.[a-z_]+$', module_name):
#       if re.match(r'^tests.[a-z_]+$', module_name):
#           if module_name not in settings.INSTALLED_APPS:
#               try:
#                   module = import_module(module_name + '.models')
#                   settings.INSTALLED_APPS += (module_name, )
#               except ImportError:
#                   pass

#   print(settings.INSTALLED_APPS)

    django.setup()

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

#   if options.settings:
#       os.environ['DJANGO_SETTINGS_MODULE'] = options.settings
#   else:
#       if "DJANGO_SETTINGS_MODULE" not in os.environ:
#           os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.test_sqlite'

    if options.nocontrib:
        os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.test_sqlite'
    else:
        os.environ['DJANGO_SETTINGS_MODULE'] = 'sandbox.settings'

    main(
        options.modules,
        verbosity=options.verbosity,
        failfast=options.failfast,
        contrib=options.contrib,
        nocontrib=options.nocontrib,
    )
