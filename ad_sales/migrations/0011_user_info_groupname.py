# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ad_sales', '0010_auto_20151223_1751'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_info',
            name='groupname',
            field=models.CharField(null=True, max_length=20),
        ),
    ]
