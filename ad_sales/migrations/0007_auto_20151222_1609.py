# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ad_sales', '0006_remove_order_layout_desires'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date_completed',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='date_recieved',
            field=models.DateField(),
        ),
    ]
