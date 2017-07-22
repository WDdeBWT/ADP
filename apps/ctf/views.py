# coding: utf-8

from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, PageNotAnInteger
from django.db.models import Count
from django.http import JsonResponse

from .models import Ctf
from operations.models import UserComments, UserLearn
from users.models import UserProfile


# Create your views here.


class CtfListView(View):
    """
    ctf列表页面,页面上方是ctf课程,下方是最新评论
    """

    def get(self, request):

        # 得到所有ctf课程
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

        # 如果没有参数传过来就默认是web类型的题目,如果参数里面还含有标签的信息则查询结果为空
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

        # 遍历每一个课程,看看用户是否学过,以便在页面中标记处用户做过的题目
        # 首先判断用户是否登录
        if request.user.is_authenticated():
            # 用户学过的所有课程
            user_learned = UserLearn.objects.filter(user_id=request.user.id, learn_type=1).values_list('learn_id',
                                                                                                       flat=True)
            # 还没有被解出来的题目列表
            # 用户未登录导致模板中访问user_leaerned属性时报出的属性不存在的错误已经由Django模板引擎解决,若不存在默认为''
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
        # 要是评论的课程删除了就删除这个评论
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
        for user_tunple in max_user:
            # 得到用户对象
            user_entity = UserProfile.objects.get(id=user_tunple[0])
            # 得到用户对象解题总数
            user_entity.total_num = user_tunple[1]
            # 得到用户做的最多的题目种类
            category2 = \
                Ctf.objects.filter(id__in=UserLearn.objects.filter(user_id=user_tunple[0], learn_type=1)).values_list(
                        'category').annotate(count=Count('category')).values_list('count', 'category').order_by(
                        '-count')[0][1]
            user_entity.category = CATEGORY_CHOICES[category2]
            # 得到用户做的题目的总分
            user_entity.earn_num = sum(
                    Ctf.objects.filter(
                            id__in=UserLearn.objects.filter(user_id=user_tunple[0], learn_type=1)).values_list('score',
                                                                                                               flat=True))
            # 将用户传入列表
            user_list.append(user_entity)

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

        # 由主键得到ctf对象
        ctf = Ctf.objects.get(id=int(ctf_id))

        # 自动增加点击量
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

        # 判断用户是否已经登录,为之后的评论和提交答案做准备
        if not request.user.is_authenticated():
            flag = 0
        else:
            flag = 1

        return render(request, 'ctf-detail.html', {
            "ctf": ctf,
            "pass_rate": pass_rate,
            "comments": comments,
            "new_ctfs": new_ctfs,
            "flag": flag,
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
            # 查看用户发送的flag错误
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
                # 这个ctf题目的成功人数加1
                ctf = Ctf.objects.get(id=int(request.POST.get('ExamCTFID')))
                ctf.success_num += 1
                # 这个ctf题目的答题次数加一
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
            # 返回成功提示给页面
            message["msg"] = "评论保存成功"
            return JsonResponse(message)
        except:
            message["msg"] = "评论保存失败"
            return JsonResponse(message)
