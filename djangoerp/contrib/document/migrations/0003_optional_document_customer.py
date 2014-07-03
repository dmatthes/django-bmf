# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from djangoerp.settings import BASE_MODULE

if BASE_MODULE["CUSTOMER"]:
    class Migration(migrations.Migration):

        dependencies = [
            ('djangoerp_document', '0002_optional_document_project'),
            migrations.swappable_dependency(BASE_MODULE["CUSTOMER"]),
        ]

        operations = [
            migrations.AddField(
                model_name='document',
                name='customer',
                field=models.ForeignKey(blank=True, to=BASE_MODULE["CUSTOMER"], null=True),
                preserve_default=True,
            ),
        ]
else:
    class Migration(migrations.Migration):
        pass
