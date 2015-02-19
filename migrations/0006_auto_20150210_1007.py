# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('threaded_emails', '0005_auto_20150210_0942'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailmessage',
            name='num_children',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='emailmessage',
            name='parent',
            field=models.ForeignKey(blank=True, to='threaded_emails.EmailMessage', null=True),
            preserve_default=True,
        ),
    ]
