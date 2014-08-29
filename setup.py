#!/usr/bin/python
# ex:set fileencoding=utf-8:

import os
import sys

from setuptools import setup, find_packages, Command

from djangoerp import __author__, __contact__, __homepage__

CLASSIFIERS = [
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.7',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    'Topic :: Office/Business :: Groupware',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

# Dynamically calculate the version based on djangoerp.VERSION.
version = __import__('djangobmf').get_version()

setup(
    name='djangoBMF',
    version=version,
    url="http://www.igelware.de/",
    license='BSD',
    platforms=['OS Independent'],
    description='Buisiness Management Framework with integrated ERP solution written for django',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    author=__author__,
    author_email=__contact__,
    packages=find_packages(exclude=['sandbox']),
    classifiers=CLASSIFIERS,
    install_requires=[
        'django',
        'pytz',
        'Pillow',
        'django-sekizai',
        'django-mptt',
        'django-filter',
        'reportlab',
        'xhtml2pdf',
        'markdown',
    ],
    include_package_data=True,
    zip_safe=False,
    test_suite='run_tests.main',
    tests_require = [
#       'coverage',
#       'pep8',
    ],
)
