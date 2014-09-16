# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangobmf_timesheet', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='timesheet',
            name='auto',
            field=models.BooleanField(default=False, editable=False),
            preserve_default=True,
        ),
    ]
