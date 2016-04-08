# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ad_sales', '0011_user_info_groupname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prototype',
            name='status',
        ),
        migrations.RemoveField(
            model_name='prototype_pic',
            name='status',
        ),
    ]
