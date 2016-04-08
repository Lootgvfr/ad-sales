# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ad_sales', '0002_auto_20151221_1805'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='ad_model',
            table='model',
        ),
        migrations.AlterModelTable(
            name='order',
            table='order',
        ),
    ]
