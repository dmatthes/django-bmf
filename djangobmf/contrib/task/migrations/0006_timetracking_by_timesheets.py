# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangobmf_task', '0005_task_in_charge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goal',
            name='billable',
        ),
        migrations.RemoveField(
            model_name='task',
            name='seconds_on',
        ),
        migrations.RemoveField(
            model_name='task',
            name='work_date',
        ),
    ]
