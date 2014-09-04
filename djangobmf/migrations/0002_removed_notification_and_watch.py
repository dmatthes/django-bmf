# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('djangobmf', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Notification',
        ),
        migrations.DeleteModel(
            name='Watch',
        ),
    ]
