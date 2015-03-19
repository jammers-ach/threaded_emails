# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('threaded_emails', '0010_emailmessage_body_html'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filepath', models.CharField(max_length=200)),
                ('filename', models.CharField(max_length=200)),
                ('email', models.ForeignKey(to='threaded_emails.EmailMessage')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
