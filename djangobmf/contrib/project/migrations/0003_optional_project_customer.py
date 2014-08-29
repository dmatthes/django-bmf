# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from djangoerp.settings import BASE_MODULE
import django

if BASE_MODULE["PROJECT"]:
    class Migration(migrations.Migration):
        dependencies = [
            ('djangoerp_project', '0001_initial'),
            migrations.swappable_dependency(BASE_MODULE["CUSTOMER"]),
        ]
        operations = [
            migrations.AddField(
                model_name='project',
                name='customer',
                field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to=BASE_MODULE["CUSTOMER"], null=True, blank=True, related_name="erp_projects"),
                preserve_default=True,
            ),
        ]
else:
    class Migration(migrations.Migration):
        pass
