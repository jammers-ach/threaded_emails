# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filepath', models.CharField(max_length=200)),
                ('filename', models.CharField(max_length=200)),
                ('url', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EmailMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('to_addr', models.EmailField(max_length=75)),
                ('from_addr', models.EmailField(max_length=75)),
                ('subject', models.TextField()),
                ('body', models.TextField(null=True, blank=True)),
                ('body_html', models.TextField(null=True, blank=True)),
                ('message_id', models.CharField(unique=True, max_length=200)),
                ('reply_to', models.CharField(max_length=200, null=True, blank=True)),
                ('num_children', models.IntegerField(default=0)),
                ('time_recived', models.DateTimeField()),
                ('time_sent', models.DateTimeField()),
                ('read', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EmailTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('template_name', models.CharField(max_length=300, verbose_name='Template name')),
                ('default_subject', models.CharField(max_length=300, verbose_name='Subject')),
                ('text', models.TextField(help_text=b'', verbose_name='Email Body')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EmailTemplateCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category_name', models.CharField(max_length=300)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MailBox',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mailbox_type', models.IntegerField(default=1, choices=[(1, b'IMAP'), (2, b'POP')])),
                ('server', models.CharField(max_length=100)),
                ('account', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('last_check_date', models.DateTimeField(null=True, blank=True)),
                ('smtp_address', models.CharField(max_length=100)),
                ('smtp_port', models.IntegerField(default=465)),
                ('from_addr', models.CharField(max_length=100)),
                ('clear_on_read', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='emailtemplate',
            name='template_category',
            field=models.ForeignKey(verbose_name='Template category', to='threaded_emails.EmailTemplateCategory'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='emailmessage',
            name='mailbox',
            field=models.ForeignKey(to='threaded_emails.MailBox'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='emailmessage',
            name='parent',
            field=models.ForeignKey(blank=True, to='threaded_emails.EmailMessage', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='attachment',
            name='email',
            field=models.ForeignKey(to='threaded_emails.EmailMessage'),
            preserve_default=True,
        ),
    ]
