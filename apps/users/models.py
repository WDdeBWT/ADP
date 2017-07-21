# coding:utf-8

from __future__ import unicode_literals
from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name=u"昵称", default="V")
    birthday = models.DateField(verbose_name=u"生日", null=True, blank=True)
    gender = models.CharField(max_length=6, choices=(("male", u"男"), ("female", "女")), default="male",
                              verbose_name=u"性别")
    mobile = models.CharField(max_length=11, default="", verbose_name=u"手机号码", blank=True)
    image = models.ImageField(upload_to="image/%Y/%m", default=u"image/default.jpg", max_length=100,
                              verbose_name=u"用户头像")
    address = models.CharField(max_length=100, verbose_name=u"用户地区", default="未知")
    introduce = models.CharField(max_length=200, verbose_name=u"自我介绍", default="这个人很懒,什么都没有留下~")
    add_time = models.DateField(verbose_name=u"加入时间", default=datetime.now)

    class Meta:
        verbose_name = u"用户信息"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.username

    def unread_nums(self):
        # 获取未读消息数量
        from operations.models import UserMessage
        return UserMessage.objects.filter(email=self.email, has_read=False).count()


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name=u"验证码")
    email = models.EmailField(max_length=50, verbose_name=u"邮箱")
    send_type = models.CharField(verbose_name=u"验证码类型",
                                 choices=(("register", u"注册"), ("forget", u"找回密码"), ("update_email", u"修改邮箱")), max_length=15)
    send_time = models.DateTimeField(verbose_name=u"发送时间", default=datetime.now)

    class Meta:
        verbose_name = u"邮箱验证码"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '{0}({1})'.format(self.code, self.email)


class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name=u"网站标题")
    image = models.ImageField(upload_to="banner/%Y/%m", verbose_name=u"轮播图", max_length=100)
    url = models.URLField(max_length=200, verbose_name=u"访问地址")
    index = models.IntegerField(default=100, verbose_name=u"顺序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"轮播图"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name
