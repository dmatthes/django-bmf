# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
        ('djangobmf', '0002_removed_notification_and_watch'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('watch_id', models.PositiveIntegerField(null=True)),
                ('triggered', models.BooleanField(db_index=True, verbose_name='Triggered', editable=False, default=True)),
                ('unread', models.BooleanField(db_index=True, verbose_name='Unread', editable=False, default=True)),
                ('last_seen_object', models.PositiveIntegerField(null=True)),
                ('new_entry', models.BooleanField(db_index=True, verbose_name='New entry', default=False)),
                ('comment', models.BooleanField(db_index=True, verbose_name='Comment written', default=False)),
                ('file', models.BooleanField(db_index=True, verbose_name='File added', default=False)),
                ('changed', models.BooleanField(db_index=True, verbose_name='Object changed', default=False)),
                ('workflow', models.BooleanField(db_index=True, verbose_name='Workflowstate changed', default=False)),
                ('modified', models.DateTimeField(verbose_name='Modified', null=True, editable=False, default=django.utils.timezone.now)),
                ('user', models.ForeignKey(null=True, blank=True, to=settings.AUTH_USER_MODEL)),
                ('watch_ct', models.ForeignKey(null=True, to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ('-modified',),
                'get_latest_by': 'modified',
                'verbose_name_plural': 'Watched activities',
                'verbose_name': 'Watched activity',
                'default_permissions': (),
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='notification',
            unique_together=set([('user', 'watch_ct', 'watch_id')]),
        ),
        migrations.AlterField(
            model_name='dashboard',
            name='user',
            field=models.ForeignKey(null=True, related_name='+', blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='numbercycle',
            name='ct',
            field=models.OneToOneField(null=True, editable=False, to='contenttypes.ContentType', related_name='bmf_numbercycle'),
        ),
        migrations.AlterField(
            model_name='report',
            name='contenttype',
            field=models.ForeignKey(null=True, help_text='Connect a Report to an BMF-Model', blank=True, to='contenttypes.ContentType', related_name='bmf_report'),
        ),
        migrations.AlterField(
            model_name='view',
            name='dashboard',
            field=models.ForeignKey(null=True, related_name='views', to='djangobmf.Dashboard'),
        ),
    ]
