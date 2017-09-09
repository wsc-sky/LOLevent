# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0010_userprofile_events'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='events',
            new_name='future_events',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='past_events',
            field=models.CharField(default=b'', max_length=200),
            preserve_default=True,
        ),
    ]
