#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.text import get_valid_filename
from django.utils.timezone import now
from django.utils.encoding import force_text, smart_str

import uuid
import os


def generate_filename(instance, filename):
    uuid_str = str(uuid.uuid4())
    datepart = force_text(now().strftime(smart_str("%Y/%m")))
    randompart = u"%s/%s" % (uuid_str[0:2], uuid_str)
    return os.path.join(datepart, randompart, get_valid_filename(filename))
