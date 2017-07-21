# _*_ coding:utf-8 _*_
__author__ = "WDdeBWT"
__date__ = "2017/7/19 11:54"

from random import Random
from django.core.mail import send_mail

from  users.models import EmailVerifyRecord
from ADP.settings import EMAIL_FROM


def send_register_email(email, send_type="register"):
    email_record = EmailVerifyRecord()
    if send_type == "update_email":
        code = random_str(4)
    else:
         code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ""
    emai_body = ""

    if send_type == "register":
        email_title = "ADP-注册激活"
        emai_body = "点击链接激活：http://127.0.0.1:8000/active/{0}".format(code)
        send_status = send_mail(email_title, emai_body, EMAIL_FROM, [email])
        if send_status:
            pass
    elif send_type == "forget":
        email_title = "ADP-密码重置"
        emai_body = "点击链接重置密码：http://127.0.0.1:8000/reset/{0}".format(code)
        send_status = send_mail(email_title, emai_body, EMAIL_FROM, [email])
        if send_status:
            pass
    elif send_type == "update_email":
        email_title = "ADP-邮箱修改"
        emai_body = "本次邮箱修改验证码为：{0}".format(code)
        send_status = send_mail(email_title, emai_body, EMAIL_FROM, [email])
        if send_status:
            pass


def random_str(randomlength=8):
    str = ""
    chars = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz1234567890"
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str
