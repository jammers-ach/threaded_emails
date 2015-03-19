# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('threaded_emails', '0008_auto_20150311_0932'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailbox',
            name='clear_on_read',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
