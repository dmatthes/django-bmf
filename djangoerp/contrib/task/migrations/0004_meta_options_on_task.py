# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangoerp_task', '0003_optional_project'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['due_date', 'summary'], 'verbose_name': 'Task', 'verbose_name_plural': 'Tasks'},
        ),
    ]
