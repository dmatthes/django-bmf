# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from djangoerp.settings import BASE_MODULE

class Migration(migrations.Migration):

    dependencies = [
        ('djangoerp_employee', '0002_optional_employee_contact'),
        migrations.swappable_dependency(BASE_MODULE["PRODUCT"]),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='product',
            field=models.ForeignKey(verbose_name='Product', blank=True, to=BASE_MODULE["PRODUCT"], null=True),
            preserve_default=True,
        ),
    ]
