#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals
# from django.core.files.storage import FileSystemStorage
from djangobmf.settings import STORAGE, STORAGE_OPTIONS, STORAGE_STATIC_PREFIX


class BMFStorage(STORAGE):
    def __init__(self):
        super(BMFStorage, self).__init__(**STORAGE_OPTIONS)

    def get_available_name(self, name):
        if name.startswith(STORAGE_STATIC_PREFIX):
            if self.exists(name):
                self.delete(name)
            return name
        return super(BMFStorage, self).get_available_name(name)
