# _*_ coding:utf-8 _*_
__author__ = "WDdeBWT"
__date__ = "2017/7/19 18:16"

from django.conf.urls import url, include

from .views import UserinfoView, UploadImageView, UpdatePswView

urlpatterns = [
    # 用户个人中心
    url(r'^info/$', UserinfoView.as_view(), name="user_info"),
    # 用户头像上传
    url(r'^image/upload/$', UploadImageView.as_view(), name="image_upload"),
    # 用户个人中心修改密码
    url(r'^update/pwd/$', UpdatePswView.as_view(), name="update_psw"),
]
