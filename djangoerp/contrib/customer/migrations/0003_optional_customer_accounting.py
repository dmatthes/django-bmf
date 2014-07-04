# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from djangoerp.settings import BASE_MODULE

if BASE_MODULE["PROJECT"]:
    class Migration(migrations.Migration):

        dependencies = [
            ('djangoerp_customer', '0002_optional_customer_project'),
            migrations.swappable_dependency(BASE_MODULE["ACCOUNT"]),
        ]

        operations = [
            migrations.AddField(
                model_name='customer',
                name='asset_account',
                field=models.ForeignKey(to=BASE_MODULE["ACCOUNT"], null=True),
                preserve_default=True,
            ),
            migrations.AddField(
                model_name='customer',
                name='liability_account',
                field=models.ForeignKey(to=BASE_MODULE["ACCOUNT"], null=True),
                preserve_default=True,
            ),
        ]
else:
    class Migration(migrations.Migration):
        pass
