# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import djangobmf.fields
import django.utils.timezone
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('djangobmf_employee', '0003_optional_employee_product'),
        ('djangobmf_task', '0005_task_in_charge'),
        ('djangobmf_project', '0005_added_acl'),
    ]

    operations = [
        migrations.CreateModel(
            name='Timesheet',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('modified', models.DateTimeField(verbose_name='Modified', auto_now=True, null=True)),
                ('created', models.DateTimeField(verbose_name='Created', null=True, auto_now_add=True)),
                ('uuid', models.CharField(verbose_name='UUID', blank=True, max_length=100, editable=False, db_index=True, null=True)),
                ('state', djangobmf.fields.WorkflowField(db_index=True, max_length=32, editable=False, blank=True, null=True)),
                ('summary', models.CharField(verbose_name='Title', max_length=255, null=True)),
                ('description', models.TextField(verbose_name='Description', blank=True, null=True)),
                ('start', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('end', models.DateTimeField(blank=True, null=True)),
                ('valid', models.BooleanField(default=False, editable=False)),
                ('created_by', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL, blank=True, on_delete=django.db.models.deletion.SET_NULL, editable=False, null=True)),
                ('employee', models.ForeignKey(related_name='+', to='djangobmf_employee.Employee', blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL)),
                ('modified_by', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL, blank=True, on_delete=django.db.models.deletion.SET_NULL, editable=False, null=True)),
                ('project', models.ForeignKey(to='djangobmf_project.Project', blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL)),
                ('task', models.ForeignKey(to='djangobmf_task.Task', blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL)),
            ],
            options={
                'abstract': False,
                'verbose_name_plural': 'Timesheets',
                'verbose_name': 'Timesheet',
                'ordering': ['start'],
                'permissions': (('can_manage', 'Can manage timesheets'),),
            },
            bases=(models.Model,),
        ),
    ]
