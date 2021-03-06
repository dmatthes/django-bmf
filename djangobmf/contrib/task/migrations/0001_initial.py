# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djangobmf.fields
import django.db.models.deletion
from django.conf import settings

from djangobmf.settings import BASE_MODULE

class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        migrations.swappable_dependency(BASE_MODULE["EMPLOYEE"]),
    ]

    operations = [
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modified', null=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created', null=True)),
                ('uuid', models.CharField(editable=False, max_length=100, blank=True, null=True, verbose_name='UUID', db_index=True)),
                ('referee', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to=BASE_MODULE["EMPLOYEE"], null=True, related_name="+")),
                ('state', djangobmf.fields.WorkflowField(db_index=True, max_length=32, null=True, editable=False, blank=True)),
                ('summary', models.CharField(max_length=255, null=True, verbose_name='Title')),
                ('description', models.TextField(null=True, verbose_name='Description', blank=True)),
                ('billable', models.BooleanField(default=False, verbose_name='Is billable')),
                ('completed', models.BooleanField(default=False, verbose_name='Completed', editable=False)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, related_name="+")),
                ('modified_by', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, related_name="+")),
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
                ('state', djangobmf.fields.WorkflowField(db_index=True, max_length=32, null=True, editable=False, blank=True)),
                ('summary', models.CharField(max_length=255, null=True, verbose_name='Title')),
                ('description', models.TextField(null=True, verbose_name='Description', blank=True)),
                ('due_date', models.DateField(null=True, verbose_name='Due date', blank=True)),
                ('work_date', models.DateTimeField(null=True, editable=False)),
                ('seconds_on', models.PositiveIntegerField(default=0, null=True, editable=False)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to=BASE_MODULE["EMPLOYEE"], null=True)),
                ('completed', models.BooleanField(default=False, verbose_name='Completed', editable=False)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, related_name="+")),
                ('goal', models.ForeignKey(blank=True, to='djangobmf_task.Goal', null=True)),
                ('modified_by', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, related_name="+")),
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
