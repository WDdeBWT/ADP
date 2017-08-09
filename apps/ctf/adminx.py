# coding: utf-8

import xadmin

from .models import Ctf


class CtfAdmin(object):
    # 在管理页面中显示的字段
    list_display = ['name', 'images','port', 'flag', 'score', 'source', 'success_num']
    # 在管理页面的搜索框中选择的字段
    search_fields = ['name', 'category', 'tag']
    # 在管理页面的筛选中显示的字段
    list_filter = ['name', 'success_num', 'fav_num', 'degree', 'click_num']
    # 排序
    ordering = ['-click_num']
    # 只读字段
    readonly_fields = ['click_num', 'fav_num', 'success_num', 'submit_num']


xadmin.site.register(Ctf, CtfAdmin)
