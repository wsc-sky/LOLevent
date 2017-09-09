# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0007_auto_20170814_0300'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='organizer',
            field=models.CharField(default='Garena', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ImageField(null=True, upload_to=b'', blank=True),
        ),
    ]
