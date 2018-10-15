# __author: ward
# data: 2018/10/15
from django.shortcuts import render, HttpResponse, redirect


# 此装饰器的作用就是讲所有没有session验证的页面都需要验证后方可跳转
def login_required(fn):
    def inner(request, *args, **kwargs):
        if not request.session.get('is_login') == '1':
            next = request.path_info
            return redirect('/login/?next={}'.format(next))
        ret = fn(request, *args, **kwargs)
        return ret

    return inner


def login(request):
    if request.method == 'POST':
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        if user == '1' and pwd == '1':
            next = request.GET.get('next')
            if next:
                ret = redirect(next)
            else:
                ret = redirect('/index/')
            request.session['is_login'] = '1'  # 设置session
            request.session.set_expiry(5)  # 设置超时间
            return ret
    return render(request, 'login.html')


@login_required
def home(request):
    return HttpResponse('这是home页面')


@login_required
def index(request):
    print(request.session.session_key)  # 获取django_session表中的键
    print(request.session.exists('vlqc57dhhm9jiy12c70zyii6bnit6xcv'))
    return render(request, 'index.html')


def logout(request):
    # request.session.delete()
    request.session.flush()  # 删除该用户的所有数据，删除cookie
    ret = redirect('/login/')
    return ret
