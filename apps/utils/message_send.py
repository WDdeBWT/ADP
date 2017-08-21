# _*_ coding:utf-8 _*_
__author__ = "WDdeBWT"
__date__ = "2017/8/21 15:16"

from operations.models import UserMessage


def send_message(text="NULL", sender="NULL", addressee="1@1.com"):
    """
        发送站内信，text信件正文，sender发件人，addressee收件人，收件人缺省即发送至管理员
    """
    user_message = UserMessage()
    user_message.email = addressee
    user_message.message = "发送人：" + sender + "| 发送信息：" + text
    user_message.save()
    pass
