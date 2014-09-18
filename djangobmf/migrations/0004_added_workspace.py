# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('djangobmf', '0003_new_notifications'),
    ]

    operations = [
        migrations.CreateModel(
            name='Workspace',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('slug', models.SlugField(max_length=30)),
                ('url', models.CharField(editable=False, db_index=True, max_length=255)),
                ('public', models.BooleanField(default=True)),
                ('editable', models.BooleanField(default=True)),
                ('module', models.CharField(blank=True, null=True, max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('ct', models.ForeignKey(to='contenttypes.ContentType', related_name='+', blank=True, null=True)),
                ('parent', mptt.fields.TreeForeignKey(to='djangobmf.Workspace', related_name='children', blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Workspace',
                'verbose_name_plural': 'Workspace',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='workspace',
            unique_together=set([('parent', 'slug')]),
        ),
    ]
