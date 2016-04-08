# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ad_sales', '0004_auto_20151221_1807'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prototype_pic',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('status', models.CharField(max_length=20)),
                ('img', models.FileField(upload_to='prototypes/')),
                ('order', models.ForeignKey(to='ad_sales.Order')),
            ],
            options={
                'db_table': 'prototype_pic',
            },
        ),
        migrations.AlterField(
            model_name='prototype',
            name='order',
            field=models.ForeignKey(to='ad_sales.Order'),
        ),
    ]
