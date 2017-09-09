# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0005_auto_20170812_0727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.CharField(default=b'<function now at 0x10a5d1578>', max_length=100),
        ),
        migrations.AlterField(
            model_name='event',
            name='pub_date',
            field=models.CharField(default=b'<function now at 0x10a5d1578>', max_length=100),
        ),
    ]
