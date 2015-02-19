# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('threaded_emails', '0002_auto_20140912_1340'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailmessage',
            name='message_id',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mailbox',
            name='from_addr',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mailbox',
            name='smtp_address',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
