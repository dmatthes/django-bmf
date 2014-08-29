#!/usr/bin/env python
import os, sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sandbox.settings")
os.environ['DJANGO_LIVE_TEST_SERVER_ADDRESS'] = 'localhost:8900-9000'

import django
from django.test.utils import get_runner
from django.conf import settings
from django.utils.unittest import TextTestResult
from django.utils.unittest import TextTestRunner
#from django.test.runner import DiscoverRunner

from coverage import coverage
from xml.etree import ElementTree as ET
import time

from discover_jenkins.results import XMLTestResult

DIRS = ['djangoerp',] 

def main():

    print('*'*80)
    print('django '+'.'.join(map(str,django.VERSION[0:3])))
    print('*'*80)

    project_dir = os.path.dirname(__file__)
    cov_files = []
    for d in DIRS:
        for (path, dirs, files) in os.walk(os.path.join(project_dir,d)):
            if os.path.basename(path) == 'tests' or os.path.basename(path) == "migrations":
                continue
            cov_files.extend([os.path.join(path, file) for file in files if file.endswith('.py') and file != "tests.py"])
    cov = coverage()
    cov.erase()
    cov.start()

    try:
        django.setup()
    except AttributeError:
        pass

    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=2, interactive=False, failfast=False)

    # code from djanog.tests.runner, which does this:
    test_runner.setup_test_environment()
    suite = test_runner.build_suite(DIRS, None)
    old_config = test_runner.setup_databases()
    result = TextTestRunner(buffer=True, resultclass=XMLTestResult, verbosity=test_runner.verbosity).run(suite)
    test_runner.teardown_databases(old_config)
    test_runner.teardown_test_environment()
    failures = test_runner.suite_result(suite, result)

    cov.stop()
    # cov.report(cov_files)
    cov.xml_report(cov_files)
    cov.html_report(cov_files)

    result.dump_xml('.')
    sys.exit(failures)

if __name__ == '__main__':
    main()
