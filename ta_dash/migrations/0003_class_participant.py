# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-07-06 21:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ta_dash', '0002_remove_class_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='participant',
            field=models.ManyToManyField(through='ta_dash.Enrollment', to='ta_dash.UserProfile'),
        ),
    ]
