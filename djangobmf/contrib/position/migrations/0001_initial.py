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
        migrations.swappable_dependency(BASE_MODULE["PRODUCT"]),
        migrations.swappable_dependency(BASE_MODULE["INVOICE"]),
    ]

    operations = [
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modified', null=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created', null=True)),
                ('uuid', models.CharField(editable=False, max_length=100, blank=True, null=True, verbose_name='UUID', db_index=True)),
                ('date', models.DateField(null=True, verbose_name='Date')),
                ('name', models.CharField(max_length=255, null=True, verbose_name='Name')),
                ('invoiceable', models.PositiveSmallIntegerField(default=1, verbose_name='Invoiceable', null=True, editable=False, choices=[(1, '100%'), (2, '80%'), (3, '50%'), (4, '0%')])),
                ('price', djangobmf.fields.MoneyField(verbose_name='Price', max_digits=27, decimal_places=9)),
                ('price_currency', djangobmf.fields.CurrencyField(default=djangobmf.fields.get_default_currency, max_length=4, null=True, editable=False)),
                ('price_precision', models.PositiveSmallIntegerField(default=0, null=True, editable=False, blank=True)),
                ('amount', models.FloatField(default=1.0, null=True, verbose_name='Amount')),
                ('description', models.TextField(null=True, verbose_name='Description', blank=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, related_name="+")),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, editable=False, to=BASE_MODULE["INVOICE"], null=True)),
                ('modified_by', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, related_name="+")),
                ('product', models.ForeignKey(to=BASE_MODULE["PRODUCT"], on_delete=django.db.models.deletion.PROTECT, null=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Position',
                'verbose_name_plural': 'Positions',
            },
            bases=(models.Model,),
        ),
    ]
