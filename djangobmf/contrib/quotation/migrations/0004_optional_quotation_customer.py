# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from djangobmf.settings import BASE_MODULE

class Migration(migrations.Migration):
    dependencies = [
        ('djangobmf_quotation', '0003_optional_quotation_employee'),
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
