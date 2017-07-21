# coding:utf-8

from __future__ import unicode_literals
from datetime import datetime
from django.db import models

from users.models import UserProfile
from ctf.models import Ctf
from experiments.models import Experiment


# Create your models here.

class UserComments(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u"用户")
    comment_id = models.IntegerField(default=0, verbose_name=u"评论对象id")
    comment_type = models.IntegerField(choices=((1, u"CTF题目"), (2, u"漏洞体验")), verbose_name=u"评论类型", default=1)
    comments = models.CharField(max_length=300, verbose_name=u"评论")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"用户评论"
        verbose_name_plural = verbose_name


class UserFavorite(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u"用户")
    fav_id = models.IntegerField(default=0, verbose_name=u"收藏对象id")
    fav_type = models.IntegerField(choices=((1, "CTF题目"), (2, "漏洞体验")), default=1, verbose_name=u"收藏类型")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"用户收藏"
        verbose_name_plural = verbose_name


class UserMessage(models.Model):
    email = models.EmailField(max_length=50, verbose_name=u"接收用户邮箱", default="1@1.com")
    message = models.CharField(max_length=500, verbose_name=u"消息内容", default="")
    has_read = models.BooleanField(default=False, verbose_name=u"是否已读")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"用户消息"
        verbose_name_plural = verbose_name


class UserLearn(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u"用户")
    learn_id = models.IntegerField(default=0, verbose_name=u"学习对象id")
    learn_type = models.IntegerField(choices=((1, u"CTF题目"), (2, u"漏洞体验")), verbose_name=u"学习类型")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"用户学习"
        verbose_name_plural = verbose_name
