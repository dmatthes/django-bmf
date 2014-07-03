# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangoerp_employee', '0002_optional_employee_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='product',
            field=models.ForeignKey(verbose_name='Product', blank=True, to='djangoerp_product.Product', null=True),
            preserve_default=True,
        ),
    ]
