# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django

from djangoerp.settings import BASE_MODULE

if BASE_MODULE["PROJECT"]:
    class Migration(migrations.Migration):

        dependencies = [
            ('djangoerp_task', '0002_optional_employee'),
            migrations.swappable_dependency(BASE_MODULE["PROJECT"]),
        ]

        operations = [
            migrations.AddField(
                model_name='goal',
                name='project',
                field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to=BASE_MODULE["PROJECT"], null=True),
                preserve_default=True,
            ),
            migrations.AddField(
                model_name='task',
                name='project',
                field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to=BASE_MODULE["PROJECT"], null=True),
                preserve_default=True,
            ),
        ]
else:
    class Migration(migrations.Migration):
        pass
