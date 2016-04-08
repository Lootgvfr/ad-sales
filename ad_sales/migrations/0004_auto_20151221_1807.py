# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ad_sales', '0003_auto_20151221_1806'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Ad_model',
            new_name='Prototype',
        ),
        migrations.AlterModelTable(
            name='prototype',
            table='prototype',
        ),
    ]
