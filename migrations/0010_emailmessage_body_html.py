# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('threaded_emails', '0009_mailbox_clear_on_read'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailmessage',
            name='body_html',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
