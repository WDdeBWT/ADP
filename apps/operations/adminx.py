# coding: utf-8

import xadmin

from .models import UserComments, UserMessage, UserLearn


class UserCommentsAdmin(object):
    list_display = ['user', 'comment_id', 'comment_type', 'comments', 'add_time']


class UserMessageAdmin(object):
    list_display = ["email", "message", "has_read", "add_time"]
    search_fields = ["email", "message", "has_read"]
    list_filter = ["email", "message", "has_read", "add_time"]


class UserLearnAdmin(object):
    list_display = ["user", "learn_id", "learn_type", "add_time"]
    search_fields = ["user", "message", "has_read"]
    list_filter = ["user", "learn_id", "learn_type", "add_time"]


xadmin.site.register(UserComments, UserCommentsAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(UserLearn, UserLearnAdmin)
