# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from djangobmf.settings import BASE_MODULE

if BASE_MODULE["EMPLOYEE"]:
    class Migration(migrations.Migration):
        dependencies = [
            ('djangobmf_invoice', '0002_optional_invoice_project'),
            migrations.swappable_dependency(BASE_MODULE["EMPLOYEE"]),
        ]
        operations = [
            migrations.AddField(
                model_name='invoice',
                name='employee',
                field=models.ForeignKey(to=BASE_MODULE["EMPLOYEE"], on_delete=django.db.models.deletion.SET_NULL, null=True),
                preserve_default=True,
            ),
        ]
else:
    class Migration(migrations.Migration):
        pass
