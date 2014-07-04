# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from djangoerp.settings import BASE_MODULE

if BASE_MODULE["PROJECT"]:
    class Migration(migrations.Migration):

        dependencies = [
            ('djangoerp_accounting', '0001_initial'),
            migrations.swappable_dependency(BASE_MODULE["PROJECT"]),
        ]

        operations = [
            migrations.AddField(
                model_name='transaction',
                name='project',
                field=models.ForeignKey(blank=True, to='djangoerp_project.Project', null=True),
                preserve_default=True,
            ),
        ]
else:
    class Migration(migrations.Migration):
        pass
