# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ad_sales', '0012_auto_20151223_2218'),
    ]

    operations = [
        migrations.AddField(
            model_name='prototype_pic',
            name='status',
            field=models.CharField(max_length=30, default='Запропонований'),
        ),
    ]
