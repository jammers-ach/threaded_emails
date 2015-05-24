# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('threaded_emails', '0012_attachment_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailtemplate',
            name='default_subject',
            field=models.CharField(max_length=300, verbose_name='Subject'),
        ),
        migrations.AlterField(
            model_name='emailtemplate',
            name='template_category',
            field=models.ForeignKey(verbose_name='Template category', to='threaded_emails.EmailTemplateCategory'),
        ),
        migrations.AlterField(
            model_name='emailtemplate',
            name='template_name',
            field=models.CharField(max_length=300, verbose_name='Template name'),
        ),
        migrations.AlterField(
            model_name='emailtemplate',
            name='text',
            field=models.TextField(help_text=b'', verbose_name='Email Body'),
        ),
    ]
