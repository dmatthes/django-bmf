# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('djangobmf_employee', '0003_optional_employee_product'),
        ('djangobmf_team', '0001_initial'),
        ('djangobmf_task', '0003_optional_project'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='goal',
            options={'verbose_name': 'Goal', 'ordering': ['project__name', 'summary'], 'permissions': (('can_manage', 'Can manage all goals'),), 'verbose_name_plural': 'Goals'},
        ),
        migrations.AddField(
            model_name='goal',
            name='employees',
            field=models.ManyToManyField(related_name='employees', blank=True, to='djangobmf_employee.Employee'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='goal',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, null=True, blank=True, to='djangobmf_team.Team'),
            preserve_default=True,
        ),
    ]
