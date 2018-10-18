from django.shortcuts import render, redirect, HttpResponse

# Create your views here.
from django.views import View
from app02 import forms
from django.contrib import auth
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from app01 import models


class MyLogin(View):
    def get(self, request):
        return render(request, 'testagain/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = auth.authenticate(username=username, password=password)
        if user_obj:
            print('obj', user_obj)
            print('request', request)
            print('request_content', dir(request))
            print('request_user', request.user, type(request.user))
            auth.login(request, user_obj)
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('/index1/')
        return render(request, 'testagain/login.html')


@method_decorator(login_required, name='get')
class MyIndex(View):
    def get(self, request):
        return render(request, 'testagain/index.html')

    def post(self, request):
        auth.logout(request)
        return render(request, 'testagain/login.html')


class MyReg(View):
    form_obj = forms.RegForm()

    def get(self, request):
        return render(request, 'testagain/reg.html', {'form_obj': self.form_obj})

    def post(self, request):
        self.form_obj = forms.RegForm(request.POST)
        if self.form_obj.is_valid():
            print(self.form_obj)
            username = request.POST.get('username')
            password = request.POST.get('re_password')
            models.UserInfo.objects.create_user(username=username, password=password, is_staff=1)
            return redirect('/login1/')
        return render(request, 'testagain/reg.html', {'form_obj': self.form_obj})


@method_decorator(login_required, name='get')
class MyPwd(View):
    form_obj = forms.ChancePwd()

    def get(self, request):
        return render(request, 'testagain/change_pwd.html', {"form_obj": self.form_obj})

    def post(self, request):
        self.form_obj = forms.ChancePwd(request.POST)
        # user = models.UserInfo.objects.get(username='')
        old_password = request.POST.get('old_password')
        if self.form_obj.is_valid():
            if request.user.check_password(old_password):
                new_password = request.POST.get('new_password')
                request.user.set_password(new_password)
                request.user.save()
                return HttpResponse('修改成功')
            else:
                self.form_obj.add_error('old_password', '旧密码错误')
        return render(request, 'testagain/change_pwd.html', {"form_obj": self.form_obj})
