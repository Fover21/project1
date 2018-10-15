# __author: ward
# data: 2018/10/15
from django.shortcuts import render, HttpResponse, redirect


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


def home(request):
    return HttpResponse('这是home页面')


def index(request):
    print(request.session.session_key)  # 获取django_session表中的键
    print(request.session.exists('vlqc57dhhm9jiy12c70zyii6bnit6xcv'))
    return render(request, 'index.html')


def logout(request):
    # request.session.delete()
    request.session.flush()  # 删除该用户的所有数据，删除cookie
    ret = redirect('/login/')
    return ret
