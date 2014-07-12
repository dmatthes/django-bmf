# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings
import djangoerp.file.storage
import djangoerp.file.models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modified', null=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created', null=True)),
                ('uuid', models.CharField(editable=False, max_length=100, blank=True, null=True, verbose_name='UUID', db_index=True)),
                ('file', models.FileField(upload_to=djangoerp.file.models.generate_filename, storage=djangoerp.file.storage.ERPStorage(), verbose_name='File')),
                ('size', models.PositiveIntegerField(null=True, editable=False, blank=True)),
                ('is_static', models.BooleanField(default=False)),
                ('content_id', models.PositiveIntegerField(null=True, editable=False, blank=True)),
                ('content_type', models.ForeignKey(blank=True, editable=False, to='contenttypes.ContentType', null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('modified_by', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
                'get_latest_by': 'modified',
                'verbose_name': 'Document',
                'verbose_name_plural': 'Documents',
            },
            bases=(models.Model,),
        ),
    ]
