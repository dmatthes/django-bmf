#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now, get_default_timezone

from .validators import template_name_validator, match_y, match_m

import datetime
import re


def _generate_name(value, date, counter):
    """
    convert the name_template into a propper string

    {year}  -> %(year)s - and set year = True
    {month}  -> %(month)s - and set month = True
    {counter:0Nd}  -> %(count)05d - required
    year, counter, month only once in the string

    """
    return value.format(**{
        'counter': counter,
        'year': date.strftime('%Y'),
        'month': date.strftime('%m'),
    })


class NumberCycle(models.Model):
    ct = models.OneToOneField(ContentType, related_name="erp_numbercycle", null=True, blank=False, editable=False)
    name_template = models.CharField(max_length=64, null=True, blank=False, validators=[template_name_validator])
    counter_start = models.PositiveIntegerField(null=True, blank=False, default=1)
    current_period = models.DateField(null=True, blank=False, default=now)

    def __unicode__(self):
        return self.name_template

    def get_periods(self):
        month = bool(re.findall(match_m, self.name_template))
        if month:
            start = datetime.datetime(self.current_period.year, self.current_period.month, 1, 0, 0, 0, tzinfo=get_default_timezone())
            if self.current_period.month == 12:
                end = datetime.datetime(self.current_period.year, 12, 31, 0, 0, 0, tzinfo=get_default_timezone())
            else:
                end = datetime.datetime(self.current_period.year, self.current_period.month + 1, 1, 0, 0, 0, tzinfo=get_default_timezone()) - datetime.timedelta(days=1)
        else:
            start = datetime.datetime(self.current_period.year, 1, 1, 0, 0, 0, tzinfo=get_default_timezone())
            end = datetime.datetime(self.current_period.year, 12, 31, 0, 0, 0, tzinfo=get_default_timezone())
        return start, end

    def generate_name(self, model, object):
        if bool(re.findall(match_y, self.name_template)):
            start, end = self.get_periods()
            if end < object.created:
                self.counter_start = 1
                self.current_period = object.created.date()
                self.save()
                start, end = self.get_periods()
            counter = model.objects.filter(created__range=(start, end), pk__lt=object.pk).count() + self.counter_start
        else:
            counter = object.pk

        return _generate_name(self.name_template, object.created, counter)
