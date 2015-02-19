# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime

class Migration(migrations.Migration):

    dependencies = [
        ('threaded_emails', '0004_auto_20140913_1405'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailmessage',
            name='read',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='emailmessage',
            name='reply_to',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='emailmessage',
            name='time_recived',
            field=models.DateTimeField(default=datetime.datetime.now()),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='emailmessage',
            name='time_sent',
            field=models.DateTimeField(default=datetime.datetime.now()),
            preserve_default=False,
        ),
    ]
