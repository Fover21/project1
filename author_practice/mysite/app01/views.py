from django.shortcuts import render, redirect, HttpResponse, reverse

# Create your views here.

from django.contrib import auth  # app
from django.contrib.auth.decorators import login_required


def login(request):
    if request.method == 'POST':
        # 方法一
        username = request.POST.get('username')
        password = request.POST.get('password')
        # obj = auth.authenticate(request, username=username, password=password)
        # print(obj, type(obj))

        # 方法二
        # obj = auth.authenticate(request, **request.POST)  # 有错，得修改见后面
        obj = auth.authenticate(request, username=username, password=password)
        print(obj, type(obj))
        if obj:
            auth.login(request, obj)  # 记录你的登录状态*（本质是在后端记录你的session数据）
            next = request.GET.get('next')
            if next:
                return redirect(next)
            return redirect('/index/')
        else:
            return HttpResponse('Username or Password is fail')
    return render(request, 'login.html')


@login_required
def index(request):
    # 登录状态
    print(request.user.is_authenticated)

    # 查看是否是数据库中命令
    print(request.user.check_password('root1234'))

    # 修改密码命令
    # request.user.set_password('密码')
    # request.user.save()

    if request.method == 'POST':
        auth.logout(request)
        return redirect('/login/')
    return render(request, 'index.html')


from django.views import View
from app01.forms import Register
from django.contrib.auth.models import User


class Homework(View):
    form_obj = Register()

    def get(self, request):
        return render(request, 'homework.html', {'form_obj': self.form_obj})

    def post(self, request):
        self.form_obj = Register(request.POST)
        if self.form_obj.is_valid():
            print(request.POST)
            print(self.form_obj.cleaned_data)
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            name = request.POST.get('name')
            gender = request.POST.get('gender')
            pwd = request.POST.get('pwd')
            # models.RegisterDb.objects.create(email=email, phone=phone, name=name, gender=gender, pwd=pwd)
            # 存入数据库（用户）
            # User.objects.create(username=email, password=pwd) # 没有加密
            # self.form_obj.cleaned_data # 可以打散使用
            # 创建用户
            User.objects.create_user(username=email, password=pwd, is_staff=1)
            # 创建超集用户
            # User.objects.create_superuser(email='', username=email, password=pwd)  # email需要自己设置
            return redirect('/login/')
        print('test')
        return render(request, 'homework.html', {'form_obj': self.form_obj})
