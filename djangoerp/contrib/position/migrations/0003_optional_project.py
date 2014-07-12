# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from djangoerp.settings import BASE_MODULE

if BASE_MODULE["PROJECT"]:
    class Migration(migrations.Migration):
        dependencies = [
            ('djangoerp_position', '0002_optional_employee'),
            migrations.swappable_dependency(BASE_MODULE["PROJECT"]),
        ]
        operations = [
            migrations.AddField(
                model_name='position',
                name='project',
                field=models.ForeignKey(to=BASE_MODULE["PROJECT"], null=True),
                preserve_default=True,
            ),
        ]
else:
    class Migration(migrations.Migration):
        pass
