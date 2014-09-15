# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django.db.models.deletion
from django.conf import settings
import djangobmf.fields


class Migration(migrations.Migration):

    dependencies = [
        ('djangobmf_employee', '0003_optional_employee_product'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('djangobmf_task', '0005_task_in_charge'),
    ]

    operations = [
        migrations.CreateModel(
            name='Timesheet',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('modified', models.DateTimeField(verbose_name='Modified', null=True, auto_now=True)),
                ('created', models.DateTimeField(verbose_name='Created', auto_now_add=True, null=True)),
                ('uuid', models.CharField(db_index=True, blank=True, null=True, editable=False, verbose_name='UUID', max_length=100)),
                ('state', djangobmf.fields.WorkflowField(db_index=True, blank=True, null=True, editable=False, max_length=32)),
                ('summary', models.CharField(verbose_name='Title', null=True, max_length=255)),
                ('description', models.TextField(blank=True, verbose_name='Description', null=True)),
                ('start', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('end', models.DateTimeField(blank=True, null=True)),
                ('valid', models.BooleanField(default=False, editable=False)),
                ('created_by', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.SET_NULL, null=True, editable=False, to=settings.AUTH_USER_MODEL, related_name='+')),
                ('employee', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.SET_NULL, null=True, to='djangobmf_employee.Employee', related_name='+')),
                ('modified_by', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.SET_NULL, null=True, editable=False, to=settings.AUTH_USER_MODEL, related_name='+')),
                ('project', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.SET_NULL, null=True, to='djangobmf_task.Task')),
            ],
            options={
                'verbose_name': 'Timesheet',
                'permissions': (('can_manage', 'Can manage timesheets'),),
                'ordering': ['start'],
                'abstract': False,
                'verbose_name_plural': 'Timesheets',
            },
            bases=(models.Model,),
        ),
    ]
