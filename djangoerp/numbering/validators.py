#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.core.exceptions import ValidationError

import re

match_y = r'{year}'
match_m = r'{month}'
match_c = r'{counter:0[1-9]+[0-9]*d}'


def template_name_validator(value):
    y = re.findall(match_y, value)
    m = re.findall(match_m, value)
    c = re.findall(match_c, value)
    if len(y) > 1:
        raise ValidationError(u'{year} can only be used once')
    if len(m) > 1:
        raise ValidationError(u'{month} can only be used once')
    if len(m) == 1 and len(y) == 0:
        raise ValidationError(u'{month} can only be used while {year} is present')
    if len(c) > 1:
        raise ValidationError(u'{counter:0Nd} can only be used once')
    if len(c) == 0:
        raise ValidationError(u'{counter:0Nd} must be used once')
    try:
        value.format(year=2000, month=10, counter=1)
    except ValueError:
        raise ValidationError(u'The string has the wrong format')
