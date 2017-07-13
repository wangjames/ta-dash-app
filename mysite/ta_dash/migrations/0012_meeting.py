# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-07-13 18:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ta_dash', '0011_auto_20170712_1852'),
    ]

    operations = [
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=200)),
                ('meeting_date', models.DateTimeField()),
                ('associated_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ta_dash.Class')),
            ],
        ),
    ]
