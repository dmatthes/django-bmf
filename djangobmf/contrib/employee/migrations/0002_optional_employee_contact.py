# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion

from djangobmf.settings import BASE_MODULE

class Migration(migrations.Migration):

    dependencies = [
        ('djangobmf_employee', '0001_initial'),
        migrations.swappable_dependency(BASE_MODULE["CUSTOMER"]),
    ]
 
    operations = [
        migrations.AddField(
            model_name='employee',
            name='contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Contact', blank=True, to=BASE_MODULE["CUSTOMER"], null=True, related_name='bmf_employee'),
            preserve_default=True,
        ),
    ]
