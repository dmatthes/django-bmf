# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangoerp_task', '0002_optional_employee'),
    ]

    operations = [
        migrations.AddField(
            model_name='goal',
            name='project',
            field=models.ForeignKey(blank=True, to='djangoerp_project.Project', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='task',
            name='project',
            field=models.ForeignKey(blank=True, to='djangoerp_project.Project', null=True),
            preserve_default=True,
        ),
    ]
