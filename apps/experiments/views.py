# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, PageNotAnInteger
from django.db.models import Count

from .models import Experiment
from operations.models import UserComments,UserLearn
from users.models import UserProfile

# Create your views here.


class ExpView(View):
    """
    漏洞体验列表功能
    """

    def  get(self,request):
        #得到所有实验
        all_exps = Experiment.objects.all()
        #按点击数取前四个热门实验
        hot_exps = all_exps.order_by("-click_nums")[:4]

        CATEGORY_CHOICES = {
            "sql":"SQL注入漏洞",
            "xss":"跨站脚本漏洞",
            "weak_password":"弱口令漏洞",
            "http":"HTTP报头追踪漏洞",
            "struct2":"Struct2远程命令执行漏洞",
            "fishing":"框架钓鱼漏洞",
            "file_upload":"文件上传漏洞",
            "script":"应用程序测试脚本泄露",
            "ip":"私有IP地址泄露漏洞",
            "login":"未加密登录请求",
            "message":"敏感信息泄露漏洞",
        }
        DEGREE={
            "cj":"初级",
            "zj":"中级",
            "gj":"高级",
        }
        for hot_exp in hot_exps:
            hot_exp.category=CATEGORY_CHOICES[hot_exp.category]
            hot_exp.degree=DEGREE[hot_exp.degree]

        exp_comment_objects = UserComments.objects.filter(comment_type=2).order_by("-add_time")
        # 得到ctf课程,直接将ctf课程属性添加进ctf评论类,这样评论就可以显示来自什么题目
        # 在后台如果删除了课程那么其对应的评论也应该被删除,不然会报错
        exp_ids = Experiment.objects.all().values_list("id", flat=True)
        # 要是评论的课程删除了就删除这个评论
        for exp_comment_object in exp_comment_objects:
            if exp_comment_object.comment_id in exp_ids:
                temp = Experiment.objects.get(id=exp_comment_object.comment_id)
                exp_comment_object.exp = temp
            else:
                exp_comment_object.delete()
        # 评论分页
        try:
            comment_page = request.GET.get('page', 1)
        except PageNotAnInteger:
            comment_page = 1
        # 每页显示5条记录
        p2 = Paginator(exp_comment_objects, 5, request=request)
        comments = p2.page(comment_page)

        # 得到答题数目最多的前5个用户,格式:['user_id', '答题数目']
        max_user = UserLearn.objects.filter(learn_type=2).values_list('user_id').annotate(
            count=Count('user_id')).values_list('user_id', 'count').order_by('-count')[:5]
        user_list = []
        for user_tunple in max_user:
            # 得到用户对象
            user_entity = UserProfile.objects.get(id=user_tunple[0])
            # 得到用户对象解题总数
            user_entity.total_num = user_tunple[1]
            # 得到用户做的最多的题目种类
            category2 = \
                Experiment.objects.filter(
                    id__in=UserLearn.objects.filter(user_id=user_tunple[0], learn_type=2)).values_list(
                    'category').annotate(count=Count('category')).values_list('count', 'category').order_by(
                    '-count')[0][1]
            user_entity.category = CATEGORY_CHOICES[category2]  # 筛选出ctf的评论并且按时间倒序排列

            # 将用户传入列表
            user_list.append(user_entity)

        tags={"xss",}

        return render(request, 'exp_list.html', {
            "heroes": user_list,
            "all_comment":comments,
            "tags":tags,
            "hot_exps":hot_exps,
        })