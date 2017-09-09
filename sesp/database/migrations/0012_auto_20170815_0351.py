# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0011_auto_20170815_0153'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='like_events',
            field=models.CharField(default=b'Zheng Xin', max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='future_events',
            field=models.CharField(default=b'Zheng Xin', max_length=200),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='past_events',
            field=models.CharField(default=b'Zheng Xin', max_length=200),
        ),
    ]
