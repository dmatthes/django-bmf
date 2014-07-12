# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from djangoerp.settings import BASE_MODULE

if BASE_MODULE["PROJECT"]:
    class Migration(migrations.Migration):
        dependencies = [
            ('djangoerp_invoice', '0001_initial'),
            migrations.swappable_dependency(BASE_MODULE["PROJECT"]),
        ]
        operations = [
            migrations.AddField(
                model_name='invoice',
                name='project',
                field=models.ForeignKey(to=BASE_MODULE["PROJECT"], null=True),
                preserve_default=True,
            ),
        ]
else:
    class Migration(migrations.Migration):
        pass
