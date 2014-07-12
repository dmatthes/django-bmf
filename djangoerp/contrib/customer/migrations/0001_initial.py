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
            name='Customer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modified', null=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created', null=True)),
                ('uuid', models.CharField(editable=False, max_length=100, blank=True, null=True, verbose_name='UUID', db_index=True)),
                ('name', models.CharField(max_length=255, null=True, verbose_name='Name')),
                ('number', models.CharField(max_length=255, null=True, verbose_name='Number', blank=True)),
                ('is_company', models.BooleanField(default=False, verbose_name='Is Company')),
                ('taxvat', models.CharField(max_length=255, null=True, verbose_name='Taxvat', blank=True)),
                ('use_company_addresses', models.BooleanField(default=True, verbose_name='Can use company adresses')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active')),
                ('is_customer', models.BooleanField(default=True, verbose_name='Is customer')),
                ('is_supplier', models.BooleanField(default=False, verbose_name='Is supplier')),
                ('customer_payment_term', models.PositiveSmallIntegerField(default=1, editable=False)),
                ('supplier_payment_term', models.PositiveSmallIntegerField(default=1, editable=False)),
                ('name2', models.CharField(max_length=255, null=True, verbose_name='Name 2', blank=True)),
                ('job_position', models.CharField(max_length=255, null=True, verbose_name='Job position', blank=True)),
                ('title', models.CharField(max_length=255, null=True, verbose_name='Title', blank=True)),
                ('phone_office', models.CharField(max_length=255, null=True, verbose_name='Phone office', blank=True)),
                ('phone_privat', models.CharField(max_length=255, null=True, verbose_name='Phone privat', blank=True)),
                ('phone_mobile', models.CharField(max_length=255, null=True, verbose_name='Phone mobile', blank=True)),
                ('email', models.EmailField(max_length=75, null=True, verbose_name='Email', blank=True)),
                ('fax', models.CharField(max_length=255, null=True, verbose_name='Fax', blank=True)),
                ('website', models.URLField(null=True, verbose_name='Website', blank=True)),
                ('notes', models.TextField(null=True, verbose_name='Notes', blank=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('employee_at', models.ForeignKey(blank=True, to='djangoerp_customer.Customer', null=True)),
                ('modified_by', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'verbose_name': 'Customer',
                'verbose_name_plural': 'Customers',
            },
            bases=(models.Model,),
        ),
    ]
