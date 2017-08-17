# _*_ coding:utf-8 _*_

import json, docker
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from pure_pagination import Paginator, PageNotAnInteger
from django.core.urlresolvers import reverse

from .models import UserProfile, EmailVerifyRecord
from operations.models import UserMessage
from .forms import LoginForm, RegisterForm, UploadImageForm, ForgetPswForm, ModifyPswForm, UserInfoForm, \
    MessageSendForm, UserBirthdayInfoForm
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin
from ctf.models import Ctf, Docker
from experiments.models import Docker as exp_docker
from experiments.models import Experiment


# Create your views here.


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
                EmailVerifyRecord.objects.filter(code=active_code, send_type="register").delete()
                return render(request, "login.html")
        else:
            return render(request, "active_fail.html")


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            if UserProfile.objects.filter(email=user_name):
                return render(request, "register.html", {"register_form": register_form, "msg": "用户已存在"})
            pass_word = request.POST.get("password", "")
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.nick_name = user_name
            user_profile.password = make_password(pass_word)
            user_profile.is_active = False
            # user_profile.is_active = True
            # 写入欢迎注册的消息
            user_message = UserMessage()
            user_message.user = user_profile
            user_message.message = "欢迎注册ADP-攻防演练平台"
            try:
                send_register_email(user_name, "register")
            except:
                return render(request, "register.html", {"register_form": register_form, "msg": "发生错误，请稍候再试"})
            else:
                user_message.save()
                user_profile.save()
            return render(request, "login.html")
        else:
            return render(request, "register.html", {"register_form": register_form})


class LogoutView(View):
    def get(self, request):
        client = docker.from_env()
        dockers = Docker.objects.filter(user=request.user.username).all()
        exp_dockers = exp_docker.objects.filter(user=request.user.username).all()
        for doc in dockers:
            id = doc.con_id
            # 删除镜像和数据库条目
            try:
                container = client.containers.get(id)
                container.kill()
                container.remove(force=True)
            except:
                pass
            finally:
                doc.delete()
        for exp_doc in exp_dockers:
            id = exp_doc.con_id
            # 删除镜像和数据库条目
            try:
                container = client.containers.get(id)
                container.kill()
                container.remove(force=True)
            except:
                pass
            finally:
                exp_doc.delete()
        logout(request)
        return HttpResponseRedirect(reverse("index"))


class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        return render(request, "login.html")

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse("index"))
                else:
                    return render(request, "login.html", {"msg": "用户未激活", "login_form": login_form})
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误！", "login_form": login_form})
        else:
            return render(request, "login.html")


class UserinfoView(LoginRequiredMixin, View):
    """
    用户个人信息
    """

    def get(self, request):
        return render(request, 'usercenter-info.html', {})

    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        user_bir_info_form = UserBirthdayInfoForm(request.POST)
        if user_info_form.is_valid():
            user_info_form.save()
            if user_bir_info_form.is_valid():
                user = request.user
                user.birthday = request.POST.get("birthday", "")
                user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


class UploadImageView(LoginRequiredMixin, View):
    """
    用户修改头像
    """

    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            # 相当于：
            # image = image_form.cleaned_data['image']
            # request.user.image = image
            # request.user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


class ForgetPswView(View):
    def get(self, request):
        forget_form = ForgetPswForm()
        return render(request, "forgetpsw.html", {"forget_form": forget_form})

    def post(self, request):
        forget_form = ForgetPswForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email", "")
            send_register_email(email, "forget")
            return render(request, "send_success.html")
        else:
            return render(request, "forgetpsw.html", {"forget_form": forget_form})


class ResetView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, "password_reset.html", {"email": email})
        else:
            return render(request, "active_fail.html")


class ModifyPswView(View):
    def post(self, request):
        modify_psw_form = ModifyPswForm(request.POST)
        email = request.POST.get("email", "")
        if modify_psw_form.is_valid():
            psw1 = request.POST.get("password1", "")
            psw2 = request.POST.get("password2", "")
            if psw1 != psw2:
                return render(request, "password_reset.html", {"msg": "两次输入的密码不相同！", "email": email})
            else:
                user = UserProfile.objects.get(email=email)
                user.password = make_password(psw1)
                user.save()
                EmailVerifyRecord.objects.filter(email=email, send_type="forget").delete()
                return render(request, "login.html")
        else:
            return render(request, "password_reset.html", {"modify_psw_form": modify_psw_form})


class UpdatePswView(View):
    """
    个人中心修改密码
    """

    def post(self, request):
        modify_psw_form = ModifyPswForm(request.POST)
        if modify_psw_form.is_valid():
            psw1 = request.POST.get("password1", "")
            psw2 = request.POST.get("password2", "")
            if psw1 != psw2:
                return HttpResponse('{"status":"fail", "msg":"两次输入的密码不一致！"}', content_type='application/json')
            else:
                user = request.user
                user.password = make_password(psw1)
                user.save()
                return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_psw_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin, View):
    """
    发送邮箱验证码
    """

    def get(self, request):
        email = request.GET.get('email', '')
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"该邮箱已被注册！"}', content_type='application/json')
        else:
            send_register_email(email, "update_email")
            return HttpResponse('{"status":"success", "email":"邮箱验证码已发送"}', content_type='application/json')


class UpdateEmailView(LoginRequiredMixin, View):
    """
    修改邮箱
    """

    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')
        existed_records = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update_email')
        if existed_records:
            user = request.user
            user.email = email
            user.username = email
            user.save()
            EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update_email').delete()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码错误！"}', content_type='application/json')


class MymessageView(LoginRequiredMixin, View):
    """
    我的消息
    """

    def get(self, request):
        all_messages = UserMessage.objects.filter(email=request.user.email).order_by('-add_time')
        # 对个人消息进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_messages, 5, request=request)
        messages = p.page(page)
        for msg in all_messages:
            msg.has_read = True
            msg.save()
        return render(request, 'usercenter-message.html', {"messages": messages})


class SendmessageView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'usercenter-sendmessage.html', {})

    def post(self, request):
        message_send_form = MessageSendForm(request.POST)
        email = request.POST.get('email', "")
        if message_send_form.is_valid():
            existed_records = UserProfile.objects.filter(email=email)
            if existed_records:
                new_message = UserMessage()
                new_message.email = email
                new_message.message = "发送人：" + request.user.email + "| 发送信息：" + request.POST.get("message", "")
                new_message.save()
                return render(request, 'usercenter-sendmessage.html', {"messages": "消息已发送"})
            else:
                return render(request, 'usercenter-sendmessage.html', {"messages": "该用户不存在！"})
        else:
            return render(request, 'usercenter-sendmessage.html', {"message_send_form": message_send_form})


class IndexView(View):
    """
    漏洞体验平台首页
    """

    def get(self, request):
        # 取出六个ctf课程,按照添加时间排序
        index_ctf = Ctf.objects.all().order_by("-add_time")[:6]
        # 取出六个实验
        index_experiment = Experiment.objects.all().order_by("-add_time")[:6]
        return render(request, 'index.html', {
            "all_ctfs": index_ctf,
            "all_experiments": index_experiment,
        })


def page_not_found(request):
    # 全局404
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


def page_error(request):
    # 全局500
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response
