# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangobmf_accounting', '0002_optional_transaction_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='type',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='Type', blank=True, choices=[(10, 'Income'), (20, 'Expense'), (30, 'Asset'), (40, 'Liability'), (50, 'Equity')]),
        ),
    ]
