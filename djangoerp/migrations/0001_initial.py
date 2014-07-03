# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django.db.models.deletion
from django.conf import settings
import djangoerp.numbering.validators


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('topic', models.CharField(max_length=100, null=True, verbose_name='Topic', blank=True)),
                ('text', models.TextField(null=True, verbose_name='Text', blank=True)),
                ('action', models.PositiveSmallIntegerField(default=1, verbose_name='Action', null=True, editable=False, choices=[(1, 'Comment'), (2, 'Created'), (3, 'Updated'), (4, 'Workflow'), (5, 'File')])),
                ('template', models.CharField(verbose_name='Template', max_length=100, null=True, editable=False)),
                ('parent_id', models.PositiveIntegerField()),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modified')),
                ('parent_ct', models.ForeignKey(to='contenttypes.ContentType')),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-modified',),
                'get_latest_by': 'modified',
                'verbose_name': 'History',
                'verbose_name_plural': 'History',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('app_label', models.CharField(verbose_name='Application', max_length=100, null=True, editable=False)),
                ('field_name', models.CharField(verbose_name='Fieldname', max_length=100, null=True, editable=False)),
                ('value', models.TextField(null=True, verbose_name='Value')),
            ],
            options={
                'default_permissions': ('change',),
                'verbose_name': 'Configuration',
                'verbose_name_plural': 'Configurations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Dashboard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, null=True)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('name', 'id'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('obj_id', models.PositiveIntegerField()),
                ('unread', models.NullBooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('changed', models.DateTimeField(auto_now=True, verbose_name='Changed')),
                ('activity', models.ForeignKey(to='djangoerp.Activity', null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('obj_ct', models.ForeignKey(to='contenttypes.ContentType')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-created',),
                'default_permissions': (),
                'get_latest_by': 'modified',
                'verbose_name': 'Notification',
                'verbose_name_plural': 'Notifications',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NumberCycle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name_template', models.CharField(max_length=64, null=True, validators=[djangoerp.numbering.validators.template_name_validator])),
                ('counter_start', models.PositiveIntegerField(default=1, null=True)),
                ('current_period', models.DateField(default=django.utils.timezone.now, null=True)),
                ('ct', models.OneToOneField(null=True, editable=False, to='contenttypes.ContentType')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reporttype', models.CharField(max_length=20, verbose_name='Reporttype')),
                ('mimetype', models.CharField(default='pdf', verbose_name='Mimetype', max_length=20, editable=False)),
                ('options', models.TextField(help_text='Options for the renderer. Empty this field to get all available options with default values', verbose_name='Options', blank=True)),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modified')),
                ('contenttype', models.ForeignKey(blank=True, to='contenttypes.ContentType', help_text='Connect a Report to an ERP-Model', null=True)),
            ],
            options={
                'get_latest_by': 'modified',
                'verbose_name': 'Report',
                'verbose_name_plural': 'Reports',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='View',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.CharField(max_length=100, null=True, blank=True)),
                ('name', models.CharField(max_length=100, null=True)),
                ('url', models.CharField(max_length=80, null=True)),
                ('kwargs', models.CharField(max_length=255, null=True, blank=True)),
                ('search', models.CharField(max_length=255, null=True, blank=True)),
                ('dashboard', models.ForeignKey(to='djangoerp.Dashboard', null=True)),
            ],
            options={
                'ordering': ('name',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Watch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('watch_id', models.PositiveIntegerField()),
                ('active', models.BooleanField(default=False, verbose_name='Active', db_index=True, editable=False)),
                ('new_entry', models.BooleanField(default=False, db_index=True, verbose_name='New entry')),
                ('comment', models.BooleanField(default=False, db_index=True, verbose_name='Comment written')),
                ('file', models.BooleanField(default=False, db_index=True, verbose_name='File added')),
                ('changed', models.BooleanField(default=False, db_index=True, verbose_name='Object changed')),
                ('workflow', models.BooleanField(default=False, db_index=True, verbose_name='Workflowstate changed')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modified')),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('watch_ct', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'get_latest_by': 'modified',
                'ordering': ('-modified',),
                'verbose_name_plural': 'Watched activities',
                'default_permissions': (),
                'verbose_name': 'Watched activity',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='watch',
            unique_together=set([('user', 'watch_ct', 'watch_id')]),
        ),
    ]
