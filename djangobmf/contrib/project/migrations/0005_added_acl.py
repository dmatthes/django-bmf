# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('djangobmf_employee', '0003_optional_employee_product'),
        ('djangobmf_team', '0001_initial'),
        ('djangobmf_project', '0004_remove_project_is_bound'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'verbose_name': 'Project', 'ordering': ['name'], 'permissions': (('can_manage', 'Can manage all projects'),), 'verbose_name_plural': 'Project'},
        ),
        migrations.AddField(
            model_name='project',
            name='employees',
            field=models.ManyToManyField(related_name='bmf_projects', blank=True, to='djangobmf_employee.Employee'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, null=True, related_name='bmf_projects', blank=True, to='djangobmf_team.Team'),
            preserve_default=True,
        ),
    ]
