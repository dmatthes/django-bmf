#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals


class RemovedInERP10Warning(PendingDeprecationWarning):
    pass


class RemovedInERP09Warning(DeprecationWarning):
    pass


class RemovedInNextVersionWarning(FutureWarning):
    pass
