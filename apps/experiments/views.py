# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, PageNotAnInteger
from django.shortcuts import redirect
import docker, random, time, socket, platform
import fcntl
import struct

from .models import Experiment, Docker
from ctf.models import Docker as ctf_docker
from operations.models import UserComments


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

        all_exps = Experiment.objects.order_by("-click_nums")
        tags = []
        for exp in all_exps:
            tags.append(CATEGORY_CHOICES[exp.category])
        tags = list(set(tags))

        category = request.GET.get('category', "")
        if category == '':
            pass
        else:
            try:
                category = CATEGORY_CHOICES2[category]
            except:
                category = ''
            all_exps = Experiment.objects.filter(category=category).order_by("-click_nums")
        try:
            category = CATEGORY_CHOICES[category]
        except:
            category = ''

        for exp in all_exps:
            exp.degree = DEGREE[exp.degree]
            exp.category = CATEGORY_CHOICES[exp.category]

        exp_comment_objects = UserComments.objects.filter(comment_type=2).order_by("-add_time")

        # 在后台如果删除了课程那么其对应的评论也应该被删除,不然会报错
        exp_ids = Experiment.objects.all().values_list("id", flat=True)
        for exp_comment_object in exp_comment_objects:
            if exp_comment_object.comment_id in exp_ids:
                temp = Experiment.objects.get(id=exp_comment_object.comment_id)
                exp_comment_object.exp = temp
            else:
                exp_comment_object.delete()
        # 评论分页
        try:
            comment_page = request.GET.get('comment_page', 1)
        except PageNotAnInteger:
            comment_page = 1
        # 每页显示3条记录
        p2 = Paginator(exp_comment_objects, 3, request=request)
        comments = p2.page(comment_page)

        try:
            exp_page = request.GET.get('exp_page', 1)
        except PageNotAnInteger:
            exp_page = 1
        # 每页显示4条记录
        p1 = Paginator(all_exps, 4, request=request)
        hot_exps = p1.page(exp_page)

        return render(request, 'exp_list.html', {
            "category": category,
            "all_comment": comments,
            "tags": tags,
            "hot_exps": hot_exps,
        })


class ExpDetailView(View):
    """
    漏洞docker页面
    """

    def get(self, request, exp_id):
        if not request.user.is_authenticated():
            return render(request, "login.html")
        else:
            # 获取漏洞
            exp = Experiment.objects.get(id=int(exp_id))

            # 调用docker
            exist = Docker.objects.filter(image=exp.images, user=request.user.username)
            if not exist:
                # 将出题人提供的镜像实例化并分配内存
                client = docker.from_env()
                old_ports = Docker.objects.values_list('port', flat=True)
                ctf_ports = ctf_docker.objects.values_list('port', flat=True)
                while True:
                    port = random.randint(1024, 65535)
                    if (port not in old_ports) and (port not in ctf_ports):
                        break

                con = client.containers.run(exp.images, detach=True, ports={str(exp.port) + '/tcp': str(port)})
                container = Docker(user=request.user.username, image=exp.images, port=port, con_id=con.id)
                container.save()

            # 以下为测试部分，之后有服务器再修正
            # 判断系统并获取IP
            if platform.system() == 'Linux':
                try:
                    myip = get_ip_address('eth0')
                except:
                    try:
                        myip = get_ip_address('wlan0')
                    except:
                        myip = "127.0.0.1"
            else:
                myname = socket.getfqdn(socket.gethostname())
                myip = socket.gethostbyname(myname)
            url = "http://%s:" % (myip) + str(Docker.objects.get(user=request.user, image=exp.images).port)
            time.sleep(1)
            return redirect(url)


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,
            struct.pack('256s', ifname[:15])
    )[20:24])
