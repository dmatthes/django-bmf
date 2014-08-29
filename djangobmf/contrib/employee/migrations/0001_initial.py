# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modified', null=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created', null=True)),
                ('uuid', models.CharField(editable=False, max_length=100, blank=True, null=True, verbose_name='UUID', db_index=True)),
                ('name', models.CharField(max_length=255, null=True, verbose_name='Name')),
                ('email', models.EmailField(max_length=75, null=True, verbose_name='Email', blank=True)),
                ('phone_office', models.CharField(max_length=255, null=True, verbose_name='Phone office', blank=True)),
                ('phone_mobile', models.CharField(max_length=255, null=True, verbose_name='Phone mobile', blank=True)),
                ('fax', models.CharField(max_length=255, null=True, verbose_name='Fax', blank=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, related_name="+")),
                ('modified_by', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, related_name="+")),
                ('supervisor', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Supervisor', blank=True, to='djangobmf_employee.Employee', null=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, unique=True, related_name="bmf_employee")),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Employee',
                'verbose_name_plural': 'Employees',
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
