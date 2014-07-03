# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangoerp_employee', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='contact',
            field=models.ForeignKey(verbose_name='Contact', blank=True, to='djangoerp_customer.Customer', null=True),
            preserve_default=True,
        ),
    ]
