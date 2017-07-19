# coding: utf-8

import xadmin

from .models import UserComments


class UserCommentsAdmin(object):
    list_display = ['user', 'comment_id', 'comment_type', 'comments', 'add_time']


xadmin.site.register(UserComments, UserCommentsAdmin)
