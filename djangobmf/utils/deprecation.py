#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

"""
usage:

import warnings
from djangoerp.utils.deprecation import RemovedInNextERPVersionWarning

warnings.warn(
    "This feature is deprecated.",
    RemovedInNextERPVersionWarning, stacklevel=2)

"""


class RemovedInERP10Warning(PendingDeprecationWarning):
    pass


class RemovedInERP09Warning(DeprecationWarning):
    pass


class RemovedInNextERPVersionWarning(FutureWarning):
    pass
