# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings

from djangoerp.settings import BASE_MODULE

class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        migrations.swappable_dependency(BASE_MODULE["ACCOUNT"]),
    ]

    operations = [
        migrations.CreateModel(
            name='Tax',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modified', null=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created', null=True)),
                ('uuid', models.CharField(editable=False, max_length=100, blank=True, null=True, verbose_name='UUID', db_index=True)),
                ('name', models.CharField(max_length=255)),
                ('rate', models.DecimalField(max_digits=8, decimal_places=5)),
                ('passive', models.BooleanField(default=False, verbose_name='Tax is allways included in the product price and never visible to the customer')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active')),
                ('account', models.ForeignKey(to=BASE_MODULE["ACCOUNT"], on_delete=django.db.models.deletion.PROTECT)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, related_name="+")),
                ('modified_by', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, related_name="+")),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'verbose_name': 'Tax',
                'verbose_name_plural': 'Taxes',
            },
            bases=(models.Model,),
        ),
    ]
