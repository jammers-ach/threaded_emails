# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MailBox',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mailbox_type', models.IntegerField(default=1, choices=[(1, b'IMAP'), (2, b'POP')])),
                ('server', models.CharField(max_length=100)),
                ('account', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
