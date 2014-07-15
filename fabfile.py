#!/usr/bin/python
# ex:set fileencoding=utf-8:

from fabric.api import *
from fabric.contrib import files

import os

BASEDIR = os.path.dirname(env.real_fabfile)

PYTHON = BASEDIR + "/.virtenv/bin/python"
DJANGO = BASEDIR + "/.virtenv/bin/django-admin.py"
MANAGE = BASEDIR + "/sandbox/manage.py"

LANGUAGES = ('en', 'de',)


@task
def static():
  js()
  css()
  with lcd(BASEDIR):
    local('cp submodules/bootstrap/fonts/glyphicons* djangoerp/static/djangoerp/fonts/')


@task
def css():
  with lcd(BASEDIR):
    local('lessc custom.less > bootstrap.css')
    local('yui-compressor --type css -o djangoerp/static/djangoerp/css/bootstrap.min.css bootstrap.css')


@task
def js(debug=None):
    with lcd(BASEDIR):
        js = [
            'js/jquery-1.11.0.js',
            'js/jquery.cookie.js',
           #'js/jquery-ui-1.10.4.custom.js',
            'submodules/bootstrap/dist/js/bootstrap.js',
            'js/variables.js',
            'js/form-api.js',
            'js/erp-editform.js',
            'js/menu.js',
        ]
        local('cat %s > js/djangoerp.js' % ' '.join(js))
        if debug:
            local('cp js/djangoerp.js djangoerp/static/djangoerp/js/djangoerp.min.js')
        else:
            local('yui-compressor --type js -o djangoerp/static/djangoerp/js/djangoerp.min.js js/djangoerp.js')


@task
def test():
    """
    Tests code with django unittests
    """
    with lcd(BASEDIR):
        local('.virtenv/bin/coverage run %s test djangoerp --liveserver=localhost:8001-9000' % MANAGE)
        local('find %s/sandbox/erp_documents -empty -delete' % BASEDIR)
        local('.virtenv/bin/coverage report -m --include="djangoerp/*"')

@task
def test_contrib(app):
    with lcd(BASEDIR):
        local('.virtenv/bin/coverage run sandbox/manage.py test -v 1 djangoerp.contrib.%(app)s' % {'app': app})
        local('.virtenv/bin/coverage report -m --include="djangoerp/contrib/%(app)s/*"' % {'app': app})


@task
def locale():
  with lcd(BASEDIR + '/djangoerp'):
    for lang in LANGUAGES:
      local('%s makemessages -l %s --domain django' % (DJANGO, lang))
      local('%s makemessages -l %s --domain djangojs' % (DJANGO, lang))

 #for i in os.listdir(BASEDIR + '/djangoerp/contrib'):
 #  path = BASEDIR + '/djangoerp/contrib/' + i

 #  if not os.path.isdir(path):
 #    continue
 #  with lcd(path):
 #    with settings(warn_only=True):
 #      for lang in LANGUAGES:
 #        local('%s makemessages -l %s' % (DJANGO, lang))

 #for i in os.listdir(BASEDIR + '/djangoerp/currencies'):
 #  path = BASEDIR + '/djangoerp/currencies/' + i

 #  if not os.path.isdir(path):
 #    continue
 #  with lcd(path):
 #    with settings(warn_only=True):
 #      for lang in LANGUAGES:
 #        local('%s makemessages -l %s' % (DJANGO, lang))

@task
def docs():
  """
  generates model class diagrams
  """
  with cd(BASEDIR + '/docs'):
    local("make html SPHINXBUILD='../.tox/docs/bin/python ../.tox/docs/bin/sphinx-build'")

# models = [
#     'server',
#     'accounting',
#     'address',
#     'company',
#     'currency',
#     'customer',
#     'document',
#     'employee',
#     'event',
#     'invoice',
#     'history',
#     'memo',
#     'partner',
#     'position',
#     'product',
#     'project',
#     'quotation',
#     'shipment',
#     'stock',
#     'task',
#     'tax',
#     'team',
#     'timesheet',
#     ]

# for i in models:
#   local('%s %s graph_models -g -e -o docs/images/module_%s.png %s' % (PYTHON, MANAGE, i, i))
# local('%s %s graph_models -g -d -e -o docs/images/overview.png %s' % (PYTHON, MANAGE, ' '.join(models)))


@task
def make(data=''):
  """
  """
  with lcd(BASEDIR):
    local('rm -f sandbox/database.sqlite')
    local('%s %s migrate --noinput' % (PYTHON, MANAGE))
    if not data:
        local('%s %s loaddata djangoerp/fixtures_demousers.json djangoerp/fixtures_demodata.json' % (PYTHON, MANAGE))
    else:
        local('%s %s loaddata djangoerp/fixtures_demousers.json' % (PYTHON, MANAGE))


@task
def start_uwsgi():
  """
  """
  with lcd(BASEDIR):
    local('virtenv/bin/uwsgi uwsgi.ini')


@task
def start():
  """
  """
  with lcd(BASEDIR):
    local('%s %s runserver 8000' % (PYTHON, MANAGE))


@task
def shell():
  """
  """
  local('%s %s shell' % (PYTHON, MANAGE))
