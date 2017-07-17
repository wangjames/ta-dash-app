# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-07-09 22:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ta_dash', '0004_accountprofileid_googleuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year_in_school', models.CharField(choices=[('FR', 'Freshman'), ('SO', 'Sophomore'), ('JR', 'Junior'), ('SR', 'Senior')], default='FR', max_length=2)),
            ],
        ),
        migrations.AddField(
            model_name='enrollment',
            name='year_in_school',
            field=models.CharField(choices=[('TR', 'Teacher'), ('ST', 'Sophomore')], default='ST', max_length=2),
        ),
    ]