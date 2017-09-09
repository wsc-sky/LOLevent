# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0006_auto_20170814_0201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
        ),
        migrations.AlterField(
            model_name='event',
            name='pub_date',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
        ),
    ]
