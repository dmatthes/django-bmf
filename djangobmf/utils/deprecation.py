#!/usr/bin/python
# ex:set fileencoding=utf-8:

"""
usage:

import warnings
from djangobmf.utils.deprecation import RemovedInNextBMFVersionWarning

warnings.warn(
    "This feature is deprecated.",
    RemovedInNextBMFVersionWarning, stacklevel=2)
"""


class RemovedInBMF10Warning(PendingDeprecationWarning):  # pragma: no cover
    pass


class RemovedInBMF09Warning(DeprecationWarning):  # pragma: no cover
    pass


class RemovedInNextBMFVersionWarning(FutureWarning):  # pragma: no cover
    pass
