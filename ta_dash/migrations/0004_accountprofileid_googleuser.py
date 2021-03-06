# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-07-07 21:44
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ta_dash', '0003_class_participant'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountProfileID',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profileID', models.IntegerField(unique=True)),
                ('userID', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GoogleUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('google_id', models.IntegerField(unique=True)),
                ('userID', models.IntegerField(unique=True)),
            ],
        ),
    ]
