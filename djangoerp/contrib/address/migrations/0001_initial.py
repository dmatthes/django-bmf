# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings
from djangoerp.settings import BASE_MODULE

class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        migrations.swappable_dependency(BASE_MODULE["CUSTOMER"]),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modified', null=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created', null=True)),
                ('uuid', models.CharField(editable=False, max_length=100, blank=True, null=True, verbose_name='UUID', db_index=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active')),
                ('is_billing', models.BooleanField(default=True, verbose_name='Is billing')),
                ('is_shipping', models.BooleanField(default=True, verbose_name='Is shipping')),
                ('default_billing', models.BooleanField(default=False, verbose_name='Default billing')),
                ('default_shipping', models.BooleanField(default=False, verbose_name='Default shipping')),
                ('name', models.CharField(max_length=255, null=True, verbose_name='Name')),
                ('name2', models.CharField(max_length=255, null=True, verbose_name='Name2', blank=True)),
                ('street', models.CharField(max_length=255, null=True, verbose_name='Street')),
                ('zip', models.CharField(max_length=255, null=True, verbose_name='Zipcode')),
                ('city', models.CharField(max_length=255, null=True, verbose_name='City')),
                ('state', models.CharField(max_length=255, null=True, verbose_name='State', blank=True)),
                ('country', models.CharField(max_length=255, null=True, verbose_name='Country')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('customer', models.ForeignKey(to=BASE_MODULE["CUSTOMER"])),
                ('modified_by', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'verbose_name': 'Address',
                'verbose_name_plural': 'Addresses',
            },
            bases=(models.Model,),
        ),
    ]
