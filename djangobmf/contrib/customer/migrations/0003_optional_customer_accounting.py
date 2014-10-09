# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from djangobmf.settings import BASE_MODULE
import django

class Migration(migrations.Migration):

    dependencies = [
        ('djangobmf_customer', '0002_optional_customer_project'),
        migrations.swappable_dependency(BASE_MODULE["ACCOUNT"]),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='asset_account',
            field=models.ForeignKey(to=BASE_MODULE["ACCOUNT"], on_delete=django.db.models.deletion.PROTECT, null=True, related_name="customer_asset"),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customer',
            name='liability_account',
            field=models.ForeignKey(to=BASE_MODULE["ACCOUNT"], on_delete=django.db.models.deletion.PROTECT, null=True, related_name="customer_liability"),
            preserve_default=True,
        ),
    ]
