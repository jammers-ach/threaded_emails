# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('threaded_emails', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('to_addr', models.EmailField(max_length=75)),
                ('from_addr', models.EmailField(max_length=75)),
                ('subject', models.TextField()),
                ('body', models.TextField(null=True, blank=True)),
                ('mailbox', models.ForeignKey(to='threaded_emails.MailBox')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='mailbox',
            name='last_check_date',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
