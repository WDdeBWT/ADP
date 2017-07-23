# coding:utf-8
import xadmin

from .models import Experiment


class ExperimentAdmin(object):
    list_display = ['name', 'detail', 'degree', 'category', 'click_nums', 'fav_nums', 'students', 'add_time']
    search_fields = ['name', 'detail', 'degree', 'category', 'click_nums', 'fav_nums', 'students']
    list_filter = ['name', 'detail', 'degree', 'category', 'click_nums', 'fav_nums', 'students', 'add_time']
    ordering = ['-click_nums']
    readonly_field = ['click_nums', 'fav_nums', 'students', 'add_time']

xadmin.site.register(Experiment,ExperimentAdmin)