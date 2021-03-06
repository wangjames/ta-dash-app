# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-07-06 21:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assignment_name', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enrolled_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ta_dash.Class')),
            ],
        ),
        migrations.CreateModel(
            name='TextSubmission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200)),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ta_dash.Assignment')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Upload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upload', models.FileField(upload_to='uploads/')),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ta_dash.Assignment')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='upload',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ta_dash.UserProfile'),
        ),
        migrations.AddField(
            model_name='textsubmission',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ta_dash.UserProfile'),
        ),
        migrations.AddField(
            model_name='enrollment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ta_dash.UserProfile'),
        ),
        migrations.AddField(
            model_name='class',
            name='users',
            field=models.ManyToManyField(to='ta_dash.UserProfile'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='class_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ta_dash.Class'),
        ),
    ]
