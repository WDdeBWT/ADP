<<<<<<< HEAD
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, PageNotAnInteger
from django.shortcuts import redirect
from itertools import chain
import docker
import socket
import urllib3
import time
import random

from .models import Experiment, Docker
from ctf.models import Docker as ctfDocker


class ExpView(View):
    """
    漏洞体验列表功能
    """

    def get(self, request):
        CATEGORY_CHOICES = {
            "sql": u"SQL注入漏洞",
            "xss": u"跨站脚本漏洞",
            "weak_password": u"弱口令漏洞",
            "http": u"HTTP报头追踪漏洞",
            "struct2": u"Struct2远程命令执行漏洞",
            "fishing": u"框架钓鱼漏洞",
            "file_upload": u"文件上传漏洞",
            "script": u"应用程序测试脚本泄露",
            "ip": u"私有IP地址泄露漏洞",
            "login": u"未加密登录请求",
            "message": u"敏感信息泄露漏洞",
            "comprehensive": u"综合"
        }
        CATEGORY_CHOICES2 = {
            u"SQL注入漏洞": "sql",
            u"跨站脚本漏洞": "xss",
            u"弱口令漏洞": "weak_password",
            u"HTTP报头追踪漏洞": "http",
            u"Struct2远程命令执行漏洞": "struct2",
            u"框架钓鱼漏洞": "fishing",
            u"文件上传漏洞": "file_upload",
            u"应用程序测试脚本泄露": "script",
            u"私有IP地址泄露漏洞": "ip",
            u"未加密登录请求": "login",
            u"敏感信息泄露漏洞": "message",
            u"综合": "comprehensive"
        }
        DEGREE = {
            "cj": u"初级",
            "zj": u"中级",
            "gj": u"高级",
        }

        all_exps = Experiment.objects.all().order_by("-click_nums")
        tags = []
        for exp in all_exps:
            tags.append(CATEGORY_CHOICES[exp.category])
        tags = list(set(tags))
        # 用户选择的分类信息
        category = request.GET.get('category', "")
        if not category:
            pass
        else:
            try:
                category = CATEGORY_CHOICES2[category]
            except:
                category = ''
            if category:
                all_exps = Experiment.objects.filter(category=category).order_by("-click_nums")
        try:
            category = CATEGORY_CHOICES[category]
        except:
            category = ''
        # 页面标签列表
        for exp in all_exps:
            exp.degree = DEGREE[exp.degree]
            exp.category = CATEGORY_CHOICES[exp.category]
        # 分页
        try:
            exp_page = request.GET.get('exp_page', 1)
        except PageNotAnInteger:
            exp_page = 1
        # 每页显示4条记录
        p1 = Paginator(all_exps, 4, request=request)
        hot_exps = p1.page(exp_page)

        return render(request, 'exp_list.html', {
            "category": category,
            "tags": tags,
            "hot_exps": hot_exps,
        })


class ExpDetailView(View):
    """
    漏洞docker页面
    """

    def get(self, request, exp_id):

        if not request.user.is_authenticated():
            return render(request, "login.html", {"logintimes": 0})
        else:
            exp = Experiment.objects.get(id=int(exp_id))
            exp.students += 1
            exp.save()

            # 调用docker
            exist = Docker.objects.filter(image=exp.images, user=request.user.username)
            # 得到本机IP
            try:
                my_ip = get_ip_address()
            except:
                my_ip = "127.0.0.1"

            if not exist:
                client = docker.from_env()
                # 得到用户在此之前实例化的docker
                existed_exp = Docker.objects.filter(user=request.user.username)
                existed_ctf = ctfDocker.objects.filter(user=request.user.username)
                # 得到已经被占用的端口
                exp_ports = list(Docker.objects.values_list('port', flat=True))
                ctf_ports = list(ctfDocker.objects.values_list('port', flat=True))
                # 删除之前为用户初始化的镜像
                for doc in chain(existed_exp, existed_ctf):
                    id = doc.con_id
                    try:
                        container = client.containers.get(id)
                        container.kill()
                        container.remove(force=True)
                    except:
                        pass
                    finally:
                        doc.delete()
                # 得到一个未被占用的端口
                ports = [i for i in range(1024, 65535) if i not in (exp_ports + ctf_ports)]
                port = ports[random.randint(0, len(ports) - 1)]
                while port_is_used(my_ip, port):
                    ports.pop(ports.index(port))
                    port = ports[random.randint(0, len(ports) - 1)]
                con = client.containers.run(exp.images, detach=True, ports={str(exp.port) + '/tcp': str(port)})
                container = Docker(user=request.user.username, image=exp.images, port=port, con_id=con.id)
                container.save()

            url = "http://%s:" % (my_ip) + str(Docker.objects.get(user=request.user, image=exp.images).port)
            # 监听docker可以访问
            http = urllib3.PoolManager()
            try:
                content = http.request('GET', url)
            except:
                content = []
            while not content:
                try:
                    content = http.request('GET', url)
                except:
                    content = []
                    time.sleep(0.5)
            return redirect(url)


def get_ip_address():
    """
    获取本机IP地址
    参考:https://www.chenyudong.com/archives/python-get-local-ip-graceful.html
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


def port_is_used(ip, port):
    """
    判断此IP的此端口是否被占用(此端口是否打开)
    被占用返回True, 没有被占用返回False
    参考:http://www.jb51.net/article/79000.html
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, int(port)))
        s.shutdown(2)
        return True
    except:
        return False
=======
from django.shortcuts import render

# Create your views here.
>>>>>>> github/master
