# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ad_sales.models


class Migration(migrations.Migration):

    dependencies = [
        ('ad_sales', '0008_auto_20151222_1629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prototype_pic',
            name='img',
            field=models.FileField(upload_to=ad_sales.models.generate_filename),
        ),
    ]
