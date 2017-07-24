# coding:utf-8

from django.conf.urls import url

from .views import ExperimentListView

urlpatterns = [
    # experiment列表页
    url(r'^list/$', ExperimentListView.as_view(), name="ctf_list"),

]