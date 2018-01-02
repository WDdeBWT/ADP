# coding: utf-8

"""ADP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
<<<<<<< HEAD
=======
from django.contrib import admin
from django.views.generic import TemplateView
>>>>>>> github/master
import xadmin
from django.views.static import serve
from users.views import LoginView, LogoutView, RegisterView, ActiveUserView, ForgetPswView, ResetView, ModifyPswView
from ADP.settings import MEDIA_ROOT
<<<<<<< HEAD
from users.views import IndexView

urlpatterns = [
    # index
    url('^$', IndexView.as_view(), name="index"),
    url('^index/$', IndexView.as_view(), name="index"),
=======


urlpatterns = [
    # index
    url('^$', TemplateView.as_view(template_name="index.html"), name="index"),
    url('^index/$', TemplateView.as_view(template_name="index.html"), name="index"),
>>>>>>> github/master
    # xadmin
    url(r'^xadmin/', xadmin.site.urls),
    # ctf
    url(r'^ctf/', include('ctf.urls', namespace="ctf")),
<<<<<<< HEAD
    # 漏洞体验
    url(r'^exp/', include('experiments.urls',namespace='exp')),
=======
>>>>>>> github/master
    # captcha
    url(r'^captcha/', include('captcha.urls')),
    # 用户管理
    url('^login/$', LoginView.as_view(), name="login"),
    url('^logout/$', LogoutView.as_view(), name="logout"),
    url('^register/$', RegisterView.as_view(), name="register"),
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name="user_active"),
    url(r'^reset/(?P<active_code>.*)/$', ResetView.as_view(), name="reset_psw"),
    url('^forgetpsw/$', ForgetPswView.as_view(), name="forget_psw"),
    url('^modifypsw/$', ModifyPswView.as_view(), name="modify_psw"),
    # 用户个人中心
    url(r'^users/', include('users.urls', namespace="users")),
    # 媒体文件配置
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
<<<<<<< HEAD
    # 漏洞实验配置
    url(r'^experiment/', include('experiments.urls', namespace='experiment')),
=======
>>>>>>> github/master
]
