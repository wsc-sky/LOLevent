# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('description', models.TextField(max_length=500)),
                ('content', models.TextField(max_length=3000)),
                ('like', models.IntegerField(default=0)),
                ('like_list', models.CharField(max_length=1000)),
                ('participant', models.IntegerField(default=0)),
                ('p_list', models.CharField(max_length=1000)),
                ('comment', models.TextField(max_length=1000)),
                ('image', models.ImageField(null=True, upload_to=b'media', blank=True)),
                ('test', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('debug', models.BooleanField(default=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserUsage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now, auto_now=True)),
                ('page', models.CharField(max_length=50)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-datetime'],
            },
            bases=(models.Model,),
        ),
    ]
