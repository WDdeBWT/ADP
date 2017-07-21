# coding:utf-8

from django.conf.urls import url

from .views import CtfListView, CtfDetailView, SubmitAnswerView, CtfCommentView

urlpatterns = [
    # CTF列表页
    url(r'^list/$', CtfListView.as_view(), name="ctf_list"),
    # CTF详情页
    url(r'^detail/(?P<ctf_id>\d+)/$', CtfDetailView.as_view(), name="ctf_detail"),
    # CTF答案认证链接
    url(r'^answer/$', SubmitAnswerView.as_view(), name="ctf_answer"),
    # CTF评论链接
    url(r'^comment/$', CtfCommentView.as_view(), name="ctf_comment"),
]