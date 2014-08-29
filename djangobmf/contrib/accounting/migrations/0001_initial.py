# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djangobmf.fields
import mptt.fields
import django.db.models.deletion
from django.conf import settings

class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modified', null=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created', null=True)),
                ('uuid', models.CharField(editable=False, max_length=100, blank=True, null=True, verbose_name='UUID', db_index=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('balance', djangobmf.fields.MoneyField(default='0', editable=False, max_digits=27, decimal_places=9)),
                ('balance_currency', djangobmf.fields.CurrencyField(default=djangobmf.fields.get_default_currency, max_length=4, null=True, editable=False)),
                ('number', models.CharField(max_length=30, null=True, unique=True, verbose_name='Number', blank=True, db_index=True)),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('type', models.PositiveSmallIntegerField(verbose_name='Type', choices=[(10, 'Income'), (20, 'Expense'), (30, 'Asset'), (40, 'Liability'), (50, 'Equity')])),
                ('read_only', models.BooleanField(default=False, verbose_name='Read-only')),
                ('comment', models.TextField(null=True, verbose_name='Comment', blank=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, related_name="+")),
                ('modified_by', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, related_name="+")),
                ('parent', mptt.fields.TreeForeignKey(blank=True, to='djangobmf_accounting.Account', null=True)),
            ],
            options={
                'ordering': ['number', 'name', 'type'],
                'abstract': False,
                'verbose_name': 'Account',
                'verbose_name_plural': 'Accounts',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modified', null=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created', null=True)),
                ('uuid', models.CharField(editable=False, max_length=100, blank=True, null=True, verbose_name='UUID', db_index=True)),
                ('state', djangobmf.fields.WorkflowField(db_index=True, max_length=32, null=True, editable=False, blank=True)),
                ('text', models.CharField(max_length=255, verbose_name='Posting text')),
                ('balanced', models.BooleanField(default=False, verbose_name='Draft', editable=False)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, related_name="+")),
                ('modified_by', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, related_name="+")),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Transaction',
                'verbose_name_plural': 'Transactions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TransactionItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', djangobmf.fields.MoneyField(max_digits=27, decimal_places=9)),
                ('amount_currency', djangobmf.fields.CurrencyField(default=djangobmf.fields.get_default_currency, max_length=4, null=True, editable=False)),
                ('credit', models.BooleanField(default=True, choices=[(True, 'Credit'), (False, 'Debit')])),
                ('balanced', models.BooleanField(default=False, editable=False)),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modified', null=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='djangobmf_accounting.Account', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='transaction',
            name='accounts',
            field=models.ManyToManyField(to='djangobmf_accounting.Account', through='djangobmf_accounting.TransactionItem'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='transactionitem',
            name='transaction',
            field=models.ForeignKey(blank=True, to='djangobmf_accounting.Transaction', null=True),
            preserve_default=True,
        ),
    ]
