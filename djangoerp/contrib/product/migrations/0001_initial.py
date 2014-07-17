# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings
import djangoerp.fields

from djangoerp.settings import BASE_MODULE

class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        migrations.swappable_dependency(BASE_MODULE["ACCOUNT"]),
        migrations.swappable_dependency(BASE_MODULE["TAX"]),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modified', null=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created', null=True)),
                ('uuid', models.CharField(editable=False, max_length=100, blank=True, null=True, verbose_name='UUID', db_index=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('code', models.CharField(db_index=True, max_length=255, verbose_name='Product Code', blank=True)),
                ('type', models.PositiveSmallIntegerField(default=1, verbose_name='Product type', choices=[(1, 'Service')])),
                ('can_sold', models.BooleanField(default=False, db_index=True, verbose_name='Can be sold')),
                ('can_purchased', models.BooleanField(default=False, db_index=True, verbose_name='Can be purchased')),
                ('description', models.TextField(verbose_name='Description', blank=True)),
                ('price', djangoerp.fields.MoneyField(verbose_name='Price', max_digits=27, decimal_places=9)),
                ('price_currency', djangoerp.fields.CurrencyField(default=djangoerp.fields.get_default_currency, max_length=4, null=True, editable=False)),
                ('price_precision', models.PositiveSmallIntegerField(default=0, null=True, editable=False, blank=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('expense_account', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=BASE_MODULE["ACCOUNT"])),
                ('income_account', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=BASE_MODULE["ACCOUNT"])),
                ('modified_by', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProductTax',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('included', models.BooleanField(default=False, verbose_name='Is the tax included in the price?')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='product',
            name='taxes',
            field=models.ManyToManyField(to=BASE_MODULE["TAX"], through='djangoerp_product.ProductTax', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='producttax',
            name='product',
            field=models.ForeignKey(blank=True, to='djangoerp_product.Product', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='producttax',
            name='tax',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to=BASE_MODULE["TAX"], null=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='producttax',
            unique_together=set([('product', 'tax')]),
        ),
    ]
