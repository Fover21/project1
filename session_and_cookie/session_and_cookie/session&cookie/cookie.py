# __author: ward
# data: 2018/10/15
from django.shortcuts import render, HttpResponse, redirect


# 此装饰器的作用就是讲所有没有cookie验证的页面都需要验证后方可跳转
def login_required(fun):
    def inner(request, *args, **kwargs):
        if not request.COOKIES.get('is_login') == '1':
            next = request.path_info
            print('next', next)
            return redirect('/login/?next={}'.format(next))  # 如果没有cookie，就需要跳转登录页面，但是将此页面的路径拼接到url上
        ret = fun(request, *args, **kwargs)
        return ret

    return inner


def login(request):
    if request.method == 'POST':
        print(request.get_full_path())
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        if user == '1' and pwd == '1':
            next = request.GET.get('next')
            if next:
                ret = redirect(next)
            else:
                ret = redirect('/index/')
            ret.set_cookie('is_login', '1', max_age=5)  # 设置cookie {"is_login": '1'} 存储方式为键值对， max_age = 设置过期时间
            return ret
    return render(request, 'login.html')


@login_required
def index(request):
    return render(request, 'index.html')


@login_required
def logout(request):
    ret = redirect('/login/')
    ret.delete_cookie('is_login')  # 删除cookie
    return ret


@login_required
def home(request):
    return HttpResponse('这是home页面')
