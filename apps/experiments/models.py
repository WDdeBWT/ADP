# coding:utf-8

from __future__ import unicode_literals
from datetime import datetime
from django.db import models


# Create your models here.

# 漏洞类型来自http://www.cnvd.org.cn/publish/main/78/2012/20120924161917256776912/20120924161917256776912_.html
category_choices = (
    ("sql", "SQL注入漏洞"),
    ("xss", "跨站脚本漏洞"),
    ("weak_password", "弱口令漏洞"),
    ("http", "HTTP报头追踪漏洞"),
    ("struct2", "Struct2远程命令执行漏洞"),
    ("fishing", "框架钓鱼漏洞"),
    ("file_upload", "文件上传漏洞"),
    ("script", "应用程序测试脚本泄露"),
    ("ip", "私有IP地址泄露漏洞"),
    ("login", "未加密登录请求"),
    ("message", "敏感信息泄露漏洞"),
)


class Experiment(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"漏洞标题")
    # 题目详情可能会用富文本显示
    detail = models.CharField(verbose_name=u"漏洞详情", default="", max_length=100)
    degree = models.CharField(verbose_name=u"漏洞难度", max_length=50, choices=(("cj", "初级"), ("zj", "中级"), ("gj", "高级")))
    category = models.CharField(verbose_name=u"漏洞类型", max_length=20, choices=category_choices)
    images = models.CharField(verbose_name=u"漏洞镜像", default="", max_length=100)
    port = models.IntegerField(verbose_name=u"开放端口", default=80)
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏数")
    image = models.ImageField(upload_to="experiments/%Y/%m", verbose_name=u"logo")
    students = models.IntegerField(default=0, verbose_name=u"学习人数")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"漏洞环境"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class Docker(models.Model):
    user = models.CharField(max_length=20,default="",verbose_name="用户")
    image = models.CharField(max_length=50,verbose_name=u"镜像",default="")
    port = models.IntegerField(verbose_name=u"映射端口",default=80)
    con_id = models.CharField(verbose_name=u"容器ID",default="",max_length=100)

    class Meta:
        verbose_name = u"容器信息"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name