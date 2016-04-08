# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ad_sales', '0007_auto_20151222_1609'),
    ]

    operations = [
        migrations.AddField(
            model_name='prototype_pic',
            name='height',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='prototype_pic',
            name='width',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='prototype',
            name='status',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='prototype_pic',
            name='status',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='spot',
            name='status',
            field=models.CharField(max_length=30),
        ),
    ]
