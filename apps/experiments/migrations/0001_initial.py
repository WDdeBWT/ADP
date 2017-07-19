# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-07-16 11:07
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='\u5b9e\u9a8c\u9898\u76ee')),
                ('detail', models.CharField(default='', max_length=500, verbose_name='\u5b9e\u9a8c\u8be6\u60c5')),
                ('degree', models.CharField(choices=[('cj', '\u521d\u7ea7'), ('zj', '\u4e2d\u7ea7'), ('gj', '\u9ad8\u7ea7')], max_length=50, verbose_name='\u5b9e\u9a8c\u96be\u5ea6')),
                ('tag', models.CharField(max_length=10, null=True, verbose_name='\u5b9e\u9a8c\u6807\u7b7e')),
                ('category', models.CharField(choices=[('sql', 'SQL\u6ce8\u5165\u6f0f\u6d1e'), ('xss', '\u8de8\u7ad9\u811a\u672c\u6f0f\u6d1e'), ('weak_password', '\u5f31\u53e3\u4ee4\u6f0f\u6d1e'), ('http', 'HTTP\u62a5\u5934\u8ffd\u8e2a\u6f0f\u6d1e'), ('struct2', 'Struct2\u8fdc\u7a0b\u547d\u4ee4\u6267\u884c\u6f0f\u6d1e'), ('fishing', '\u6846\u67b6\u9493\u9c7c\u6f0f\u6d1e'), ('file_upload', '\u6587\u4ef6\u4e0a\u4f20\u6f0f\u6d1e'), ('script', '\u5e94\u7528\u7a0b\u5e8f\u6d4b\u8bd5\u811a\u672c\u6cc4\u9732'), ('ip', '\u79c1\u6709IP\u5730\u5740\u6cc4\u9732\u6f0f\u6d1e'), ('login', '\u672a\u52a0\u5bc6\u767b\u5f55\u8bf7\u6c42'), ('message', '\u654f\u611f\u4fe1\u606f\u6cc4\u9732\u6f0f\u6d1e')], max_length=20, verbose_name='\u6f0f\u6d1e\u7c7b\u578b')),
                ('click_nums', models.IntegerField(default=0, verbose_name='\u70b9\u51fb\u6570')),
                ('fav_nums', models.IntegerField(default=0, verbose_name='\u6536\u85cf\u6570')),
                ('image', models.ImageField(upload_to='experiments/%Y/%m', verbose_name='logo')),
                ('students', models.IntegerField(default=0, verbose_name='\u5b66\u4e60\u4eba\u6570')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u6dfb\u52a0\u65f6\u95f4')),
            ],
            options={
                'verbose_name': '\u5b9e\u9a8c\u540d\u79f0',
                'verbose_name_plural': '\u5b9e\u9a8c\u540d\u79f0',
            },
        ),
    ]
