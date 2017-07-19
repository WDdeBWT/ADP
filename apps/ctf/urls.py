# coding:utf-8

from django.conf.urls import url

from .views import CtfListView, CtfDetailView

urlpatterns = [
    # CTF列表页
    url(r'^list/$', CtfListView.as_view(), name="ctf_list"),
    # CTF详情页
    url(r'^detail/$', CtfDetailView.as_view(), name="ctf_detail"),
]