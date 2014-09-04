# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from djangobmf.settings import BASE_MODULE
import django

if BASE_MODULE["PROJECT"]:
    class Migration(migrations.Migration):
        dependencies = [
            ('djangobmf_customer', '0001_initial'),
            migrations.swappable_dependency(BASE_MODULE["PROJECT"]),
        ]
        operations = [
            migrations.AddField(
                model_name='customer',
                name='project',
                field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to=BASE_MODULE["PROJECT"], help_text='Projects function as cost-centers. This setting defines a default project for this customer.', null=True, related_name="+"),
                preserve_default=True,
            ),
        ]
else:
    class Migration(migrations.Migration):
        pass
