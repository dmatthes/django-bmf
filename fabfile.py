#!/usr/bin/python
# ex:set fileencoding=utf-8:

from fabric.api import *
from fabric.contrib import files

import os

BASEDIR = os.path.dirname(env.real_fabfile)

PYTHON = BASEDIR + "/virtenv/bin/python"
DJANGO = BASEDIR + "/virtenv/bin/django-admin.py"
MANAGE = BASEDIR + "/sandbox/manage.py"
DEVELOP = BASEDIR + "/develop.py"

LANGUAGES = ('en', 'de',)

FIXTURES = (
    'fixtures/sites.json',
    'fixtures/users.json',
    'fixtures/demodata.json',
    'fixtures/contrib_accounting.json',
    'fixtures/contrib_invoice.json',
    'fixtures/contrib_project.json',
    'fixtures/contrib_quotation.json',
    'fixtures/contrib_task.json',
    'fixtures/contrib_team.json',
    'fixtures/admin_dashboard.json',
)


@task
def static():
    """
    update static files
    """
    js()
    css()
    with lcd(BASEDIR):
        local('cp submodules/bootstrap/fonts/glyphicons* djangobmf/static/djangobmf/fonts/')


@task
def css():
    """
    recreate css files - with lessc and yui-compressor
    """
    with lcd(BASEDIR):
        local('lessc less/custom.less > bootstrap.css')
        local('yui-compressor --type css -o djangobmf/static/djangobmf/css/djangobmf.min.css bootstrap.css')
        local('rm bootstrap.css')


@task
def js():
    """
    recreate js files for development and production
    """
    with lcd(BASEDIR):
        js_ext = (
            'submodules/jquery-cookie/src/jquery.cookie.js',
            'submodules/jquery-treegrid/js/jquery.treegrid.js',
            'submodules/bootstrap/dist/js/bootstrap.js',
        )
        js_own = (
            'js/variables.js',
            'js/bmf-autocomplete.js',
            'js/bmf-calendar.js',
            'js/bmf-editform.js',
            'js/bmf-inlineform.js',
            'js/bmf-buildform.js',
            'js/menu.js',
        )

        local('cp submodules/bootstrap/dist/js/bootstrap.min.js djangobmf/static/djangobmf/js/')
        local('yui-compressor --type js -o djangobmf/static/djangobmf/js/jquery.cookie.min.js submodules/jquery-cookie/src/jquery.cookie.js')
        local('yui-compressor --type js -o djangobmf/static/djangobmf/js/jquery.treegrid.min.js submodules/jquery-treegrid/js/jquery.treegrid.js')

        local('cat %s > djangobmf/static/djangobmf/js/djangobmf.js' % ' '.join(js_ext + js_own))
        local('yui-compressor --type js -o djangobmf/static/djangobmf/js/djangobmf.min.js djangobmf/static/djangobmf/js/djangobmf.js')
        local('cat %s > djangobmf/static/djangobmf/js/djangobmf.js' % ' '.join(js_own))


@task
def test():
    """
    Tests code with django unittests
    """
    with lcd(BASEDIR):
        local('virtenv/bin/coverage run runtests.py -v2')
        local('virtenv/bin/coverage report -m --include="djangobmf/*"')
        local('virtenv/bin/coverage html --include="djangobmf/*"')


@task
def test_mod(app):
    with lcd(BASEDIR):
        local('virtenv/bin/coverage run runtests.py -v2 --contrib %(app)s' % {'app': app})
        local('virtenv/bin/coverage report -m --include="djangobmf/contrib/%(app)s/*"' % {'app': app})


@task
def test_core(module=""):
    with lcd(BASEDIR):
        local('virtenv/bin/coverage run runtests.py %s -v2 --nocontrib' % module)
        local('virtenv/bin/coverage report -m --include="djangobmf/*" --omit="djangobmf/contrib/*"')


@task
def locale():
    with lcd(BASEDIR + '/djangobmf'):
        local('%s makemessages -l %s --domain django' % (DJANGO, 'en'))
        local('%s makemessages -l %s --domain djangojs' % (DJANGO, 'en'))


@task
def make(data=''):
  """
  """
  with lcd(BASEDIR):
    local('rm -f sandbox/database.sqlite')
    local('%s %s migrate --noinput' % (PYTHON, MANAGE))
    if not data:
        local('%s %s loaddata %s' % (PYTHON, MANAGE, ' '.join(FIXTURES)))
    else:
        local('%s %s loaddata fixtures/users.json' % (PYTHON, MANAGE))


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
