# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ad_model',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('status', models.CharField(max_length=20)),
                ('width', models.IntegerField()),
                ('height', models.IntegerField()),
                ('layout', models.CharField(max_length=100)),
                ('text', models.CharField(max_length=200)),
                ('desc_graphical', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'ad_model',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('status', models.CharField(max_length=20)),
                ('date_recieved', models.DateTimeField()),
                ('date_completed', models.DateTimeField(null=True)),
                ('layout_desires', models.CharField(max_length=200)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'order',
            },
        ),
        migrations.CreateModel(
            name='Spot',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('page', models.IntegerField()),
                ('status', models.CharField(max_length=20)),
                ('cost', models.FloatField()),
                ('position', models.CharField(max_length=5)),
                ('width', models.IntegerField()),
                ('height', models.IntegerField()),
                ('order', models.ForeignKey(to='ad_sales.Order', null=True)),
            ],
            options={
                'db_table': 'spot',
            },
        ),
        migrations.CreateModel(
            name='User_info',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=20)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_info',
            },
        ),
        migrations.AddField(
            model_name='ad_model',
            name='order',
            field=models.ForeignKey(to='ad_sales.Order', null=True),
        ),
    ]
