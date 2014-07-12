#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

VERSION = (0, 1, 1, 'alpha', 0)
#VERSION = (0, 2, 0, 'beta', 0) # closed beta
#VERSION = (0, 3, 0, 'beta', 0) # open beta
#VERSION = (0, 9, 0, 'rc', 0)
#VERSION = (1, 0, 0, 'final', 0)

def get_version(*args, **kwargs):
    assert len(VERSION) == 5
    assert VERSION[3] in ('alpha', 'beta', 'rc', 'final')

    version = '.'.join(map(str, VERSION[:3]))

    if VERSION[3] in ['alpha', 'beta'] and VERSION[4] == 0:
        import os
        import subprocess
        import datetime

        # get version information from git
        repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        get_branch = subprocess.Popen('git rev-parse --abbrev-ref HEAD', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=repo_dir, universal_newlines=True)
        get_time = subprocess.Popen('git log --pretty=format:%ct --quiet -1 HEAD', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=repo_dir, universal_newlines=True)

        branch = get_branch.communicate()[0]
        if branch:
            version += '.' + branch.strip()
        else:
            version += '.' + VERSION[3]

        timestamp = get_time.communicate()[0]
        try:
            timestamp = datetime.datetime.utcfromtimestamp(int(timestamp))
            version += '.' + timestamp.strftime('%Y%m%d%H%M%S')
        except ValueError:
            pass

    return version

__version__ = '.'.join(map(str,VERSION[:4]))
__author__ = 'Sebastian Braun'
__contact__ = 'sebastian@elmnt.de'
__homepage__ = 'http://www.igelware.de'
__docformat__ = 'restructuredtext'

# -eof meta-

default_app_config = 'djangoerp.apps.ERPConfig'
