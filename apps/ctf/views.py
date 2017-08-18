# coding: utf-8

from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, PageNotAnInteger
from django.db.models import Count
from django.http import JsonResponse
import docker
import socket

from .models import Ctf, Docker
from experiments.models import Docker as exp_docker
from operations.models import UserComments, UserLearn
from users.models import UserProfile


class CtfListView(View):
    """
    ctf列表页面,页面上方是ctf课程,下方是最新评论
    参考:https://zhuanlan.zhihu.com/p/27988558
    """

    def get(self, request):

        all_ctf_objects = Ctf.objects.all()
        # 得到页面上传过来的课程类型
        category = request.GET.get('category', "")
        # 题目分类常量
        CATEGORY_CHOICES = {
            "MISC": "安全杂项",
            "PPC": "编程",
            "CRYPTO": "密码学",
            "PWN": "溢出",
            "REVERSE": "逆向工程",
            "STEGA": "隐写术",
            "WEB": "WEB",
        }

        # 如果没有参数传过来就默认是web类型的题目
        tag = None
        if category == '':
            category = 'WEB'
            ctf_subjects = all_ctf_objects.filter(category=category)
        # 只传递了分类信息
        elif category in CATEGORY_CHOICES.keys():
            ctf_subjects = all_ctf_objects.filter(category=category)
        # 传递了分类信息和标签信息
        elif len(category.split("__")) == 2 and (category.split("__")[0] in CATEGORY_CHOICES.keys()) and (
                    category.split("__")[1] in Ctf.objects.all().values_list("tag", flat=True)):
            tag = category.split("__")[1]
            category = category.split("__")[0]
            ctf_subjects = all_ctf_objects.filter(category=category, tag=tag)
        # 用户传递了垃圾信息
        else:
            category = 'WEB'
            ctf_subjects = all_ctf_objects.filter(category=category)

        # 得到该分类的所有标签,要是参数里面还有标签信息就把分类信息分离出来,标签不能重复!
        tags = set()
        for i in all_ctf_objects.filter(category=category):
            tags.add(i.tag)

        # 得到整个类别的参与人数(一个类别里面所有题目点击数之和)
        participation = sum(Ctf.objects.filter(category=category).values_list('click_num', flat=True))

        # 遍历每一个课程,看看用户是否学过,以便在页面中标记用户做过的题目
        if request.user.is_authenticated():
            # 用户学过的所有课程
            user_learned = UserLearn.objects.filter(user_id=request.user.id, learn_type=1).values_list('learn_id',
                                                                                                       flat=True)
            # 还没有被解出来的题目列表
            # 用户未登录导致模板中访问user_learned属性时报出的属性不存在的错误已经由Django模板引擎解决,若不存在默认为''
            not_learned = all_ctf_objects.filter(success_num=0).values_list('id', flat=True)
            for ctf_subject in ctf_subjects:
                # 用户做过的题目,在页面标记为蓝色
                if ctf_subject.id in user_learned:
                    ctf_subject.user_learned = True
                else:
                    ctf_subject.user_learned = False
                # 所有人都没有解决的题目,在页面标记为红色
                if ctf_subject.id in not_learned:
                    ctf_subject.not_learned = True
                else:
                    ctf_subject.not_learned = False

        # 筛选出ctf的评论并且按时间倒序排列
        ctf_comment_objects = UserComments.objects.filter(comment_type=1).order_by("-add_time")
        # 得到ctf课程,直接将ctf课程属性添加进ctf评论类,这样评论就可以显示来自什么题目
        # 在后台如果删除了课程那么其对应的评论也应该被删除,不然会报错
        ctf_ids = Ctf.objects.all().values_list("id", flat=True)
        for ctf_comment_object in ctf_comment_objects:
            if ctf_comment_object.comment_id in ctf_ids:
                temp = Ctf.objects.get(id=ctf_comment_object.comment_id)
                ctf_comment_object.ctf = temp
            else:
                ctf_comment_object.delete()
        # 评论分页
        try:
            comment_page = request.GET.get('page', 1)
        except PageNotAnInteger:
            comment_page = 1
        # 每页显示5条记录
        p2 = Paginator(ctf_comment_objects, 5, request=request)
        comments = p2.page(comment_page)

        # 得到答题数目最多的前5个用户,格式:['user_id', '答题数目']
        max_user = UserLearn.objects.filter(learn_type=1).values_list('user_id').annotate(
                count=Count('user_id')).values_list('user_id', 'count').order_by('-count')[:5]
        user_list = []
        try:
            for user_tunple in max_user:
                # 得到用户对象
                user_entity = UserProfile.objects.get(id=user_tunple[0])
                # 得到用户对象解题总数
                user_entity.total_num = user_tunple[1]
                # 得到用户做的最多的题目种类
                category2 = Ctf.objects.filter(
                        id__in=UserLearn.objects.filter(user_id=user_tunple[0], learn_type=1).values_list(
                                'learn_id', flat=True)).values_list('category').annotate(
                        count=Count('category')).values_list(
                        'count', 'category').order_by('-count')[0][1]
                user_entity.category = CATEGORY_CHOICES[category2]
                # 得到用户做的题目的总分
                user_entity.earn_num = sum(Ctf.objects.filter(id__in=UserLearn.objects.filter(
                        user_id=user_tunple[0], learn_type=1).values_list('learn_id', flat=True)).values_list(
                        'score', flat=True))

                user_list.append(user_entity)
        except:
            user_list = []

        return render(request, 'ctf-list.html', {
            # 分页得到的ctf课程
            "all_ctf": ctf_subjects,
            # 分页得到的ctf评论和课程数据
            "all_comment": comments,
            # 类别选择信息
            "category": category,
            # 用户排名
            "heros": user_list,
            # 一个类别的参与人数
            "participation": participation,
            # 该分类的所有标签
            "tags": tags,
            # 用户选择的标签
            "user_tag": tag,
        })


class CtfDetailView(View):
    """
    ctf详情页面
    """

    def get(self, request, ctf_id):

        if not request.user.is_authenticated():
            return render(request, "login.html")
        else:
            ctf = Ctf.objects.get(id=int(ctf_id))
            ctf.click_num += 1
            ctf.save()

            # 计算通过率, 百分数显示
            try:
                pass_rate = ctf.success_num * 100 / ctf.submit_num
            except ZeroDivisionError:
                pass_rate = 0

            # 得到用户对课程的评论
            all_comments = UserComments.objects.filter(comment_type=1, comment_id=ctf.id).order_by("-add_time")

            # 评论分页
            try:
                comment_page = request.GET.get('page', 1)
            except PageNotAnInteger:
                comment_page = 1
            # 每页显示5条记录
            p2 = Paginator(all_comments, 5, request=request)
            comments = p2.page(comment_page)

            # 网页右侧最新题目的显示,显示最近添加的同种类的五个题目
            new_ctfs = Ctf.objects.filter(category=Ctf.objects.get(id=ctf_id).category).exclude(id=ctf_id).order_by(
                    "-add_time")[:5]

            # 调用docker
            exist = Docker.objects.filter(image=ctf.images, user=request.user.username)
            # 得到本机IP
            try:
                my_ip = get_ip_address()
            except:
                my_ip = "127.0.0.1"

            # 本地测试IP, 上线时删除
            my_ip = "0.0.0.0"

            if not exist:
                client = docker.from_env()
                # 将用户在此之前实例化的docker删除
                existed = Docker.objects.filter(user=request.user.username)
                for doc in existed:
                    id = doc.con_id
                    try:
                        container = client.containers.get(id)
                        container.kill()
                        container.remove(force=True)
                    except:
                        pass
                    finally:
                        doc.delete()
                # 将出题人提供的镜像实例化并分配内存
                old_ports = Docker.objects.values_list('port', flat=True)
                exp_ports = exp_docker.objects.values_list('port', flat=True)
                # 得到一个未被占用的端口
                used_port = []
                while port_is_used(my_ip, [i for i in range(1024, 65536) if
                                           i not in (list(old_ports) + list(exp_ports) + used_port)][0]):
                    used_port.append([i for i in range(1024, 65536) if
                                      i not in (list(old_ports) + list(exp_ports) + used_port)][0])
                port = [i for i in range(1024, 65536) if i not in (list(old_ports) + list(exp_ports) + used_port)][0]
                con = client.containers.run(ctf.images, detach=True, ports={str(ctf.port) + '/tcp': str(port)})
                container = Docker(user=request.user.username, image=ctf.images, port=port, con_id=con.id)
                container.save()

            url = "http://%s:" % (my_ip) + str(Docker.objects.get(user=request.user, image=ctf.images).port)

            return render(request, 'ctf-detail.html', {
                "ctf": ctf,
                "pass_rate": pass_rate,
                "comments": comments,
                "new_ctfs": new_ctfs,
                "url": url,
            })


class SubmitAnswerView(View):
    """
    在ctf页面提交答案的处理函数
    """

    def post(self, request):
        """
        答案从ctf页面由JavaScript异步提交,使用的是post方法
        """
        res = {}
        try:
            # 查看用户是否已经拿到flag
            if int(request.POST.get('ExamCTFID')) in UserLearn.objects.filter(learn_type=1,
                                                                              user_id=request.user.id).values_list(
                    'learn_id', flat=True):
                res["code"] = '001'
                return JsonResponse(res)
            # 用户发送的flag错误
            elif str(Ctf.objects.get(id=int(request.POST.get('ExamCTFID'))).flag) != str(request.POST.get('key')):
                ctf = Ctf.objects.get(id=int(request.POST.get('ExamCTFID')))
                # 这个ctf题目的答题次数加一
                ctf.submit_num += 1
                ctf.save()
                res["code"] = '003'
                res["Score"] = 0
                return JsonResponse(res)
            # 用户发送的flag正确
            elif str(Ctf.objects.get(id=int(request.POST.get('ExamCTFID'))).flag) == str(request.POST.get('key')):
                ctf = Ctf.objects.get(id=int(request.POST.get('ExamCTFID')))
                ctf.success_num += 1
                ctf.submit_num += 1
                ctf.save()
                # 把这道题目标记到用户学习里面
                user_learn = UserLearn()
                user_learn.user_id = request.user.id
                user_learn.learn_id = int(request.POST.get('ExamCTFID'))
                user_learn.learn_type = 1
                user_learn.save()

                res["code"] = '003'
                res["Score"] = 1
                return JsonResponse(res)
            # 判断失败,此次flag提交失败
            else:
                res["code"] = '002'
                return JsonResponse(res)
        except:
            res["code"] = '002'
            return JsonResponse(res)


class CtfCommentView(View):
    """
    在ctf页面评论的处理函数
    """

    def post(self, request):
        """
        评论以异步的方式用post发送过来
        """
        message = {}
        try:
            # 将用户发送过来的评论保存起来
            user_comment = UserComments()
            user_comment.user_id = request.user.id
            user_comment.comment_type = 1
            user_comment.comment_id = request.POST.get('ExamCTFID')
            user_comment.comments = request.POST.get('Content')
            user_comment.save()
            message["msg"] = "评论保存成功"
            return JsonResponse(message)
        except:
            message["msg"] = "评论保存失败"
            return JsonResponse(message)


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
    参考:http://www.jb51.net/article/79000.htm
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, int(port)))
        s.shutdown(2)
        return True
    except:
        return False
