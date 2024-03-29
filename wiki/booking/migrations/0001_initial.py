# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-11-29 19:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DoctorFiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dname', models.CharField(max_length=10, verbose_name='医生姓名')),
                ('dtitle', models.CharField(max_length=20, verbose_name='职称')),
                ('dintroduction', models.CharField(max_length=1000, verbose_name='介绍')),
                ('department', models.CharField(max_length=20, verbose_name='所在科室')),
                ('d_create_time', models.DateTimeField(auto_now_add=True, verbose_name='上线时间')),
                ('dcount', models.DateTimeField(auto_now_add=True, verbose_name='最大预约量')),
            ],
            options={
                'db_table': 'doctor',
            },
        ),
    ]
