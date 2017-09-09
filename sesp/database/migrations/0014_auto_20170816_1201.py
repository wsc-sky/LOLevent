# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0013_comment_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='d_sort',
            field=models.IntegerField(default=0, max_length=100),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='p_sort',
            field=models.IntegerField(default=0, max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='future_events',
            field=models.CharField(default=b';', max_length=200),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='like_events',
            field=models.CharField(default=b';', max_length=200),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='past_events',
            field=models.CharField(default=b';', max_length=200),
        ),
    ]
