# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('djangobmf_accounting', '0004_added_transactionitem_as_framework_model'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='balanced',
            new_name='draft',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='accounts',
        ),
        migrations.RemoveField(
            model_name='transactionitem',
            name='balanced',
        ),
        migrations.AddField(
            model_name='transactionitem',
            name='draft',
            field=models.BooleanField(default=True, editable=False, verbose_name='Draft'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transactionitem',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, null=True, related_name='transactions', blank=True, to=settings.BMF_CONTRIB_ACCOUNT),
        ),
        migrations.AlterField(
            model_name='transactionitem',
            name='transaction',
            field=models.ForeignKey(null=True, related_name='items', blank=True, to=settings.BMF_CONTRIB_TRANSACTION),
        ),
    ]
