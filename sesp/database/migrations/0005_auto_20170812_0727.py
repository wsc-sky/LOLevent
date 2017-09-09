# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0004_auto_20170811_0838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='comment',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='event',
            name='content',
            field=models.CharField(max_length=3000),
        ),
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.CharField(max_length=500),
        ),
    ]
