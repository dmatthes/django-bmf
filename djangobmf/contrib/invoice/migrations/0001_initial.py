# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings
import djangobmf.fields
from djangobmf.settings import BASE_MODULE

class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        migrations.swappable_dependency(BASE_MODULE["TRANSACTION"]),
        migrations.swappable_dependency(BASE_MODULE["ADDRESS"]),
        migrations.swappable_dependency(BASE_MODULE["PRODUCT"]),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modified', null=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created', null=True)),
                ('uuid', models.CharField(editable=False, max_length=100, blank=True, null=True, verbose_name='UUID', db_index=True)),
                ('state', djangobmf.fields.WorkflowField(db_index=True, max_length=32, null=True, editable=False, blank=True)),
                ('invoice_number', models.CharField(max_length=255, null=True, verbose_name='Invoice number')),
                ('net', models.FloatField(null=True, editable=False, blank=True)),
                ('date', models.DateField(null=True, verbose_name='Date')),
                ('due', models.DateField(null=True, verbose_name='Due', blank=True)),
                ('notes', models.TextField(null=True, verbose_name='Notes', blank=True)),
                ('term_of_payment', models.TextField(null=True, verbose_name='Term of payment', blank=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, related_name="+")),
                ('invoice_address', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to=BASE_MODULE["ADDRESS"], null=True)),
                ('modified_by', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, related_name="+")),
                ('shipping_address', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to=BASE_MODULE["ADDRESS"], null=True)),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, editable=False, to=BASE_MODULE["TRANSACTION"], null=True)),
            ],
            options={
                'ordering': ['invoice_number'],
                'abstract': False,
                'verbose_name': 'Invoice',
                'verbose_name_plural': 'Invoices',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InvoiceProduct',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True, verbose_name='Name')),
                ('price', djangobmf.fields.MoneyField(verbose_name='Price', max_digits=27, decimal_places=9)),
                ('price_currency', djangobmf.fields.CurrencyField(default=djangobmf.fields.get_default_currency, max_length=4, null=True, editable=False)),
                ('price_precision', models.PositiveSmallIntegerField(default=0, null=True, editable=False, blank=True)),
                ('amount', models.FloatField(default=1.0, null=True, verbose_name='Amount')),
                ('description', models.TextField(null=True, verbose_name='Description', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='invoice',
            name='products',
            field=models.ManyToManyField(to=BASE_MODULE["PRODUCT"], through='djangobmf_invoice.InvoiceProduct'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='invoiceproduct',
            name='invoice',
            field=models.ForeignKey(blank=True, to='djangobmf_invoice.Invoice', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='invoiceproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='djangobmf_product.Product', null=True),
            preserve_default=True,
        ),
    ]
