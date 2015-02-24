# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('threaded_emails', '0006_auto_20150210_1007'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailbox',
            name='smtp_port',
            field=models.IntegerField(default=465),
            preserve_default=True,
        ),
    ]
