# coding:utf-8
import xadmin

from .models import Experiment


class ExperimentAdmin(object):
    list_display = ['name',  'degree','images','port','category',  'students',]
    search_fields = ['name',  'degree', 'category']
    list_filter = ['degree', 'category','click_nums', 'fav_nums', 'students','add_time']
    ordering = ['-click_nums']
    readonly_fields = ['click_nums', 'fav_nums', 'students']

xadmin.site.register(Experiment,ExperimentAdmin)