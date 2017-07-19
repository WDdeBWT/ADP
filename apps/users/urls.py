# _*_ coding:utf-8 _*_
__author__ = "WDdeBWT"
__date__ = "2017/7/19 18:16"

from django.conf.urls import url, include

from .views import UserinfoView

urlpatterns = [
    url(r'^info/$', UserinfoView.as_view(), name="user_info"),
]
