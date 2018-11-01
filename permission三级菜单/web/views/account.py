from django.shortcuts import render, HttpResponse, redirect, reverse
from rbac import models
from django.conf import settings
import copy
from rbac.server.init_permission import init_permission


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pwd = request.POST.get('pwd')

        user = models.User.objects.filter(name=username, password=pwd).first()

        if not user:
            err_msg = '用户名或密码错误'
            return render(request, 'login.html', {'err_msg': err_msg})

        # 登录成功
        # 将权限信息写入到session
        print(1111)
        init_permission(request, user)

        return redirect(reverse('web:customer'))

    return render(request, 'login.html')
