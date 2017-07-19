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
from django.contrib import admin
from django.views.generic import TemplateView
import xadmin
from django.views.static import serve
from users.views import LoginView, RegisterView, ActiveUserView
from ADP.settings import MEDIA_ROOT


urlpatterns = [
    # index
    url('^$', TemplateView.as_view(template_name="index.html"), name="index"),
    url('^index/$', TemplateView.as_view(template_name="index.html"), name="index"),
    # xadmin
    url(r'^xadmin/', xadmin.site.urls),
    # ctf
    url(r'^ctf/', include('ctf.urls', namespace="ctf")),
    # captcha
    url(r'^captcha/', include('captcha.urls')),
    # user
    url('^login/$', LoginView.as_view(), name="login"),
    url('^register/$', RegisterView.as_view(), name="register"),
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name="user_active"),
    url(r'^users/', include('users.urls', namespace="users")),
    # 媒体文件配置
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
]
