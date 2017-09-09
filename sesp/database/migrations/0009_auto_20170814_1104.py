# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0008_auto_20170814_1021'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('event_id', models.IntegerField(max_length=50)),
                ('user_name', models.CharField(max_length=100)),
                ('content', models.CharField(max_length=300)),
                ('date', models.CharField(default=django.utils.timezone.now, max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='event',
            name='comment',
        ),
        migrations.AddField(
            model_name='event',
            name='p_email',
            field=models.CharField(default=0, max_length=50),
            preserve_default=True,
        ),
    ]
