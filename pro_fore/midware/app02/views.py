from django.shortcuts import render, redirect, HttpResponse
from functools import wraps


# Create your views here.

def decorate(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        if not request.session['login_id'] == 1:
            next_url = request.path_info
            return redirect('/login/?next_url={url}'.format(url=next_url))
        ret = func(request, *args, **kwargs)
        return ret

    return inner


def login(request):
    if request.method == 'POST':
        if request.POST.get('user') == 1 and request.POST.get('pwd') == 1:
            next_url = request.GET.get('next_url')
            # 登录成功后设置session, session是在response对象上设置的
            if next_url:
                ret = redirect(next_url)
            else:
                ret = HttpResponse('登录成功！')
            # 设置session
            request.session['login_id'] = 1
            # 设置超时时间
            request.session.set_expiry(5)
            return ret

    return render(request, 'login.html')


@decorate
def home(request):
    return HttpResponse('<h1>This is home</h1>')
