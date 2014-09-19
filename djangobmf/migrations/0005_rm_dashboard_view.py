# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangobmf', '0004_added_workspace'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='view',
            name='dashboard',
        ),
        migrations.DeleteModel(
            name='View',
        ),
    ]
