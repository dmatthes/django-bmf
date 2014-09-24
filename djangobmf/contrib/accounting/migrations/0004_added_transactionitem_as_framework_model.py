# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('djangobmf_accounting', '0003_alter_field_type_on_account'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionitem',
            name='created',
            field=models.DateTimeField(verbose_name='Created', auto_now_add=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='transactionitem',
            name='created_by',
            field=models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL, null=True, editable=False, on_delete=django.db.models.deletion.SET_NULL, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='transactionitem',
            name='modified_by',
            field=models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL, null=True, editable=False, on_delete=django.db.models.deletion.SET_NULL, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='transactionitem',
            name='uuid',
            field=models.CharField(verbose_name='UUID', blank=True, editable=False, max_length=100, db_index=True, null=True),
            preserve_default=True,
        ),
    ]
