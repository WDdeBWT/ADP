# -*- coding:utf-8 -*-
from django.conf.urls import url
from .views import ExpView,ExpDetailView

urlpatterns=[
    #漏洞列表
    url(r'^list/$',ExpView.as_view(),name="exp_list"),
    url(r'^detail/(?P<exp_id>\d+)/$', ExpDetailView.as_view(), name="exp_detail"),
]