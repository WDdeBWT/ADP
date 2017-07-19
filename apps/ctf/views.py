# coding: utf-8

from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Sum

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
        # 如果没有参数传过来就默认是web类型的题目
        if not category:
            category = 'WEB'
        if category == 'MISC':
            ctf_subjects = all_ctf_objects.filter(category=category)
        elif category == 'PPC':
            ctf_subjects = all_ctf_objects.filter(category=category)
        elif category == 'CRYPTO':
            ctf_subjects = all_ctf_objects.filter(category=category)
        elif category == 'PWN':
            ctf_subjects = all_ctf_objects.filter(category=category)
        elif category == 'REVERSE':
            ctf_subjects = all_ctf_objects.filter(category=category)
        elif category == 'STEGA':
            ctf_subjects = all_ctf_objects.filter(category=category)
        else:
            ctf_subjects = all_ctf_objects.filter(category=category)

        # 筛选出ctf的评论并且按时间倒序排列
        ctf_comment_objects = UserComments.objects.filter(comment_type=1).order_by("-add_time")
        # 得到ctf课程,直接将ctf课程属性添加进ctf评论类
        for ctf_comment_object in ctf_comment_objects:
            ctf_comment_object.ctf = Ctf.objects.get(id=ctf_comment_object.comment_id)
        # 评论分页
        try:
            comment_page = request.GET.get('page', 1)
        except PageNotAnInteger:
            comment_page = 1
        # 每页显示5条记录
        p2 = Paginator(ctf_comment_objects, 5, request=request)
        comments = p2.page(comment_page)

        # 得到答题数目最多的前10个用户,格式:['user_id', '答题数目', 'learn_id']
        max_user = UserLearn.objects.filter(learn_type=1).values_list('user_id').annotate(count=Count('user_id')).values_list('user_id', 'count').order_by('-count')[:10]
        user_list = []
        for user_tunple in max_user:
            # 得到用户对象
            user_entity = UserProfile.objects.get(id=user_tunple[0])
            # 得到用户对象解题总数
            user_entity.total_num = user_tunple[1]
            # 得到用户做的最多的题目种类
            user_entity.category = Ctf.objects.filter(id__in=UserLearn.objects.filter(user_id=user_tunple[0])).values_list('category').annotate(count=Count('category')).values_list('count', 'category').order_by('-count')[0][1]
            # 得到用户做的题目的总分
            user_entity.earn_num = sum(Ctf.objects.filter(id__in=UserLearn.objects.filter(user_id=user_tunple[0])).values_list('score', flat=True))
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
        })


class CtfDetailView(View):
    def get(self, request):
        return render(request, 'ctf-detail.html', {

        })
