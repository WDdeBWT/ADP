# _*_ coding:utf-8 _*_

import xadmin

from .models import EmailVerifyRecord, Banner
from xadmin import views


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "ADP"
    site_footer = "---武汉理工大学第五实验室---"
    menu_style = "accordion"#设置左侧栏自动折叠


class EmailVerifyRecordAdmin(object):
    list_display = ["code", "email"]
    search_fields = ["code", "email"]
    list_filter = ["code", "email"]


class BannerAdmin(object):
    list_display = ["title", "image", "url", "index", "add_time"]
    search_fields = ["title", "image", "url", "index", "add_time"]
    list_filter = ["title", "image", "url", "index", "add_time"]

xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
