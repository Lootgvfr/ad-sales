# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ad_sales', '0005_auto_20151221_2243'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='layout_desires',
        ),
    ]
