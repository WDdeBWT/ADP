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
            name='Ctf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='\u8bfe\u7a0b\u540d')),
                ('detail', models.CharField(default='', max_length=500, verbose_name='\u9898\u76ee\u8be6\u60c5')),
                ('is_banner', models.BooleanField(default=False, verbose_name='\u662f\u5426\u8f6e\u64ad')),
                ('source', models.CharField(default='', max_length=100, verbose_name='\u9898\u76ee\u6765\u6e90')),
                ('degree', models.CharField(choices=[('cj', '\u521d\u7ea7'), ('zj', '\u4e2d\u7ea7'), ('gj', '\u9ad8\u7ea7')], max_length=2, verbose_name='\u96be\u5ea6')),
                ('students', models.IntegerField(default=0, verbose_name='\u5b66\u4e60\u4eba\u6570')),
                ('fav_num', models.IntegerField(default=0, verbose_name='\u6536\u85cf\u4eba\u6570')),
                ('image', models.ImageField(upload_to='ctf/%Y/%m', verbose_name='\u5c01\u9762')),
                ('click_num', models.IntegerField(default=0, verbose_name='\u70b9\u51fb\u6570')),
                ('success_num', models.IntegerField(default=0, verbose_name='\u6210\u529f\u593a\u65d7\u4eba\u6570')),
                ('flag', models.CharField(default='', max_length=100, verbose_name='\u9898\u76ee\u7b54\u6848')),
                ('category', models.CharField(choices=[('MISC', '\u5b89\u5168\u6742\u9879'), ('PPC', '\u7f16\u7a0b\u7c7b'), ('CRYPTO', '\u5bc6\u7801\u5b66\u7c7b'), ('PWN', '\u6ea2\u51fa\u7c7b'), ('REVERSE', '\u9006\u5411\u5de5\u7a0b\u7c7b'), ('STEGA', '\u9690\u5199\u7c7b'), ('WEB', 'Web\u6f0f\u6d1e\u7c7b')], max_length=7, verbose_name='\u9898\u76ee\u7c7b\u522b')),
                ('tag', models.CharField(default='', max_length=20, verbose_name='\u8bfe\u7a0b\u6807\u7b7e')),
                ('score', models.IntegerField(default=0, verbose_name='\u9898\u76ee\u5206\u6570')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u6dfb\u52a0\u65f6\u95f4')),
            ],
            options={
                'verbose_name': 'CTF\u9898\u76ee',
                'verbose_name_plural': 'CTF\u9898\u76ee',
            },
        ),
        migrations.CreateModel(
            name='BannerCtf',
            fields=[
            ],
            options={
                'verbose_name': '\u8f6e\u64adCTF\u9898\u76ee',
                'proxy': True,
                'verbose_name_plural': '\u8f6e\u64adCTF\u9898\u76ee',
            },
            bases=('ctf.ctf',),
        ),
    ]
