# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-07-09 22:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ta_dash', '0005_auto_20170709_2208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrollment',
            name='year_in_school',
            field=models.CharField(choices=[('TR', 'Teacher'), ('ST', 'Student')], default='ST', max_length=2),
        ),
    ]
