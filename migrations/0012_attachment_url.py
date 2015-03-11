# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('threaded_emails', '0011_attachment'),
    ]

    operations = [
        migrations.AddField(
            model_name='attachment',
            name='url',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
