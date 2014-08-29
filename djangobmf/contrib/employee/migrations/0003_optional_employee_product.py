# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion

from djangobmf.settings import BASE_MODULE

if BASE_MODULE["PRODUCT"]:
    class Migration(migrations.Migration):

        dependencies = [
            ('djangobmf_employee', '0002_optional_employee_contact'),
            migrations.swappable_dependency(BASE_MODULE["PRODUCT"]),
        ]

        operations = [
            migrations.AddField(
                model_name='employee',
                name='product',
                field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Product', blank=True, to=BASE_MODULE["PRODUCT"], null=True, related_name="bmf_employee"),
                preserve_default=True,
            ),
        ]
