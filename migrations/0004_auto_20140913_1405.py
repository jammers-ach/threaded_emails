# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('threaded_emails', '0003_auto_20140913_1344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailmessage',
            name='message_id',
            field=models.CharField(unique=True, max_length=200),
        ),
    ]
