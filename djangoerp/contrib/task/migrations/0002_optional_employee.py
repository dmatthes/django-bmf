# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangoerp_task', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='goal',
            name='referee',
            field=models.ForeignKey(blank=True, to='djangoerp_employee.Employee', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='task',
            name='employee',
            field=models.ForeignKey(blank=True, to='djangoerp_employee.Employee', null=True),
            preserve_default=True,
        ),
    ]
