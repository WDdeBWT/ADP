# ADP
网络安全攻防平台项目

## 组件版本
* Python == 2.7
* Django == 1.9
* xadmin 使用GitHub上源码安装
* 其他第三方包 使用pip安装

## 命名约定
* 类名：大驼峰式命名法。如**CourseAdmin**。
* 函数名：字母全部小写，单词间使用下划线隔开。如**def save_models(self):**。
* 常量名：字母全部大写，单词间使用下划线隔开。如**ROOT_URL**。
* 字段名：字母全部小写，单词使用下划线隔开。如**list_display**。

## 注释约定
* 在含有中文的页面顶部声明utf-8编码
* 类的注释及字段的注释例子如下

```python:example1.py
class CourseInfoView(LoginRequiredMixin, View):
    """
    课程章节信息
    """

    def get(self, request, course_id):
        """
        如果有注释的话就添加
        """
        course = Course.objects.get(id=int(course_id))
        # 课程学习人数加一
        course.students += 1
        course.save()
        # 查询用户是否已经关联此课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
        # 实现侧边栏功能,学过此课程的同学还学过什么
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程的id
        course_ids = [user_course.course.id for user_course in all_user_courses]
        # 获取学过该用户学过其他的所有课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]
        all_resources = CourseResource.objects.filter(course=course)
        return render(request, "course-video.html", {
            "course": course,
            "all_resources": all_resources,
            "relate_courses": relate_courses,
        })
```

## 导入包约定
* 首先导入系统包，空一行再导入自己的包。

```python:example2.py
from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.db.models import Q
[此处应有空格]
from .models import Course, CourseResource, Video
from operation.models import UserFavorite, CourseComments, UserCourse
from utils.mixin_utils import LoginRequiredMixin
```

## 其他
* 尽量多写注释
* 将逻辑尽可能的写清楚，宁可代码变长
* 写完代码后使用**Pycharm->code->reformat code**对代码进行规整


