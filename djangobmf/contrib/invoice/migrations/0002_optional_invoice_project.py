# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from djangobmf.settings import BASE_MODULE
import django.db.models.deletion

import django

if BASE_MODULE["PROJECT"]:
    class Migration(migrations.Migration):
        dependencies = [
            ('djangobmf_invoice', '0001_initial'),
            migrations.swappable_dependency(BASE_MODULE["PROJECT"]),
        ]
        operations = [
            migrations.AddField(
                model_name='invoice',
                name='project',
                field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to=BASE_MODULE["PROJECT"], null=True),
                preserve_default=True,
            ),
        ]
else:
    class Migration(migrations.Migration):
        pass
