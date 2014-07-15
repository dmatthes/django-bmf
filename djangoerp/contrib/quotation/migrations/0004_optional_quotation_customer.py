# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from djangoerp.settings import BASE_MODULE

if BASE_MODULE["CUSTOMER"]:
    class Migration(migrations.Migration):
        dependencies = [
            ('djangoerp_quotation', '0003_optional_quotation_employee'),
            migrations.swappable_dependency(BASE_MODULE["CUSTOMER"]),
        ]
        operations = [
            migrations.AddField(
                model_name='quotation',
                name='customer',
                field=models.ForeignKey(to=BASE_MODULE["CUSTOMER"], on_delete=django.db.models.deletion.SET_NULL, null=True),
                preserve_default=True,
            ),
        ]
else:
    class Migration(migrations.Migration):
        pass
