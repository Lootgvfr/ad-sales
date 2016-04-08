# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ad_sales', '0009_auto_20151222_2010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spot',
            name='position',
            field=models.CharField(max_length=30),
        ),
    ]
