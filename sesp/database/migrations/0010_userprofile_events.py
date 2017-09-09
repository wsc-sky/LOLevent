# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0009_auto_20170814_1104'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='events',
            field=models.CharField(default=b'', max_length=200),
            preserve_default=True,
        ),
    ]
