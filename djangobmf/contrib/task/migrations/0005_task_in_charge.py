# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('djangobmf_employee', '0003_optional_employee_product'),
        ('djangobmf_task', '0004_added_acl'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='in_charge',
            field=models.ForeignKey(to='djangobmf_employee.Employee', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', editable=False, blank=True),
            preserve_default=True,
        ),
    ]
