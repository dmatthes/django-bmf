# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from djangoerp.settings import BASE_MODULE

class Migration(migrations.Migration):

    dependencies = [
        ('djangoerp_employee', '0001_initial'),
        migrations.swappable_dependency(BASE_MODULE["CUSTOMER"]),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='contact',
            field=models.ForeignKey(verbose_name='Contact', blank=True, to=BASE_MODULE["CUSTOMER"], null=True),
            preserve_default=True,
        ),
    ]
