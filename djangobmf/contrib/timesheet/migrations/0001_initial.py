# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
import djangobmf.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.BMF_CONTRIB_EMPLOYEE),
        migrations.swappable_dependency(settings.BMF_CONTRIB_PROJECT),
        migrations.swappable_dependency(settings.BMF_CONTRIB_TASK),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Timesheet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified', models.DateTimeField(null=True, auto_now=True, verbose_name='Modified')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created')),
                ('uuid', models.CharField(null=True, db_index=True, editable=False, verbose_name='UUID', blank=True, max_length=100)),
                ('state', djangobmf.fields.WorkflowField(null=True, db_index=True, editable=False, max_length=32, blank=True)),
                ('summary', models.CharField(null=True, verbose_name='Title', max_length=255)),
                ('description', models.TextField(null=True, verbose_name='Description', blank=True)),
                ('start', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('end', models.DateTimeField(null=True, blank=True)),
                ('valid', models.BooleanField(default=False, editable=False)),
                ('created_by', models.ForeignKey(null=True, editable=False, blank=True, to=settings.AUTH_USER_MODEL, related_name='+', on_delete=django.db.models.deletion.SET_NULL)),
                ('employee', models.ForeignKey(null=True, to=settings.BMF_CONTRIB_EMPLOYEE, blank=True, related_name='+', on_delete=django.db.models.deletion.SET_NULL)),
                ('modified_by', models.ForeignKey(null=True, editable=False, blank=True, to=settings.AUTH_USER_MODEL, related_name='+', on_delete=django.db.models.deletion.SET_NULL)),
                ('project', models.ForeignKey(null=True, to=settings.BMF_CONTRIB_PROJECT, blank=True, on_delete=django.db.models.deletion.SET_NULL)),
                ('task', models.ForeignKey(null=True, to=settings.BMF_CONTRIB_TASK, blank=True, on_delete=django.db.models.deletion.SET_NULL)),
            ],
            options={
                'ordering': ['-end'],
                'verbose_name_plural': 'Timesheets',
                'verbose_name': 'Timesheet',
                'abstract': False,
                'swappable': 'BMF_CONTRIB_TIMESHEET',
                'permissions': (('can_manage', 'Can manage timesheets'),),
            },
            bases=(models.Model,),
        ),
    ]
