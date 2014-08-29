#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

"""
usage:

import warnings
from djangobmf.utils.deprecation import RemovedInNextBMFVersionWarning

warnings.warn(
    "This feature is deprecated.",
    RemovedInNextBMFVersionWarning, stacklevel=2)

"""


class RemovedInBMF10Warning(PendingDeprecationWarning):
    pass


class RemovedInBMF09Warning(DeprecationWarning):
    pass


class RemovedInNextBMFVersionWarning(FutureWarning):
    pass
