# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0003_auto_20170811_0835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userusage',
            name='datetime',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
