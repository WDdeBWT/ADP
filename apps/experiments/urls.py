# -*- coding:utf-8 -*-
from django.conf.urls import url
from .views import ExpView

urlpatterns=[
    #漏洞列表
    url(r'^list/$',ExpView.as_view(),name="exp_list"),
]