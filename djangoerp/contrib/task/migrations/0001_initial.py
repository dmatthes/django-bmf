# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djangoerp.fields
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modified', null=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created', null=True)),
                ('uuid', models.CharField(editable=False, max_length=100, blank=True, null=True, verbose_name='UUID', db_index=True)),
                ('state', djangoerp.fields.WorkflowField(db_index=True, max_length=32, null=True, editable=False, blank=True)),
                ('summary', models.CharField(max_length=255, null=True, verbose_name='Summary')),
                ('description', models.TextField(null=True, verbose_name='Description', blank=True)),
                ('billable', models.BooleanField(default=False, verbose_name='Is billable')),
                ('completed', models.BooleanField(default=False, verbose_name='Completed', editable=False)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('modified_by', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['project__name', 'summary'],
                'abstract': False,
                'verbose_name': 'Goal',
                'verbose_name_plural': 'Goals',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modified', null=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created', null=True)),
                ('uuid', models.CharField(editable=False, max_length=100, blank=True, null=True, verbose_name='UUID', db_index=True)),
                ('state', djangoerp.fields.WorkflowField(db_index=True, max_length=32, null=True, editable=False, blank=True)),
                ('summary', models.CharField(max_length=255, null=True, verbose_name='Summary')),
                ('description', models.TextField(null=True, verbose_name='Description', blank=True)),
                ('due_date', models.DateField(null=True, verbose_name='Due date', blank=True)),
                ('work_date', models.DateTimeField(null=True, editable=False)),
                ('seconds_on', models.PositiveIntegerField(default=0, null=True, editable=False)),
                ('completed', models.BooleanField(default=False, verbose_name='Completed', editable=False)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('goal', models.ForeignKey(blank=True, to='djangoerp_task.Goal', null=True)),
                ('modified_by', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['due_date', 'summary'],
                'abstract': False,
                'verbose_name': 'Task',
                'verbose_name_plural': 'Tasks',
            },
            bases=(models.Model,),
        ),
    ]
