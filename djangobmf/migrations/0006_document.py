# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djangobmf.utils.generate_filename
import djangobmf.document.storage
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        migrations.swappable_dependency(settings.BMF_CONTRIB_PROJECT),
        migrations.swappable_dependency(settings.BMF_CONTRIB_CUSTOMER),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('djangobmf', '0005_rm_dashboard_view'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(verbose_name='Name', null=True, editable=False, max_length=120, blank=True)),
                ('file', models.FileField(upload_to=djangobmf.utils.generate_filename.generate_filename, storage=djangobmf.document.storage.BMFStorage(), verbose_name='File')),
                ('size', models.PositiveIntegerField(null=True, editable=False, blank=True)),
                ('is_static', models.BooleanField(default=False)),
                ('content_id', models.PositiveIntegerField(null=True, editable=False, blank=True)),
                ('modified', models.DateTimeField(verbose_name='Modified', auto_now=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created', null=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType', blank=True, related_name='bmf_document', null=True, editable=False, on_delete=django.db.models.deletion.SET_NULL)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, related_name='+', null=True, editable=False, on_delete=django.db.models.deletion.SET_NULL)),
                ('customer', models.ForeignKey(to=settings.BMF_CONTRIB_CUSTOMER, blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL)),
                ('modified_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, related_name='+', null=True, editable=False, on_delete=django.db.models.deletion.SET_NULL)),
                ('project', models.ForeignKey(to=settings.BMF_CONTRIB_PROJECT, blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL)),
            ],
            options={
                'verbose_name': 'Document',
                'verbose_name_plural': 'Documents',
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
    ]
