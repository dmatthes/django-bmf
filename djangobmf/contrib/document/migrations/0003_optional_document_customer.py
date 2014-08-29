# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from djangobmf.settings import BASE_MODULE
import django

if BASE_MODULE["CUSTOMER"]:
    class Migration(migrations.Migration):

        dependencies = [
            ('djangobmf_document', '0002_optional_document_project'),
            migrations.swappable_dependency(BASE_MODULE["CUSTOMER"]),
        ]

        operations = [
            migrations.AddField(
                model_name='document',
                name='customer',
                field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to=BASE_MODULE["CUSTOMER"], null=True),
                preserve_default=True,
            ),
        ]
else:
    class Migration(migrations.Migration):
        pass
