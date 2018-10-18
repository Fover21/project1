from django.shortcuts import render, HttpResponse
from app02 import models

# Create your views here.


def register(request):
    if request.method == 'POST':
        email0 = request.POST.get('email1')
        phone0 = request.POST.get('phone')
        name0 = request.POST.get('name')
        show_name0 = request.POST.get('show_name')
        pwd0 = request.POST.get('pwd')
        pwd_Again0 = request.POST.get('pwd_Again')
        print(email0, phone0, name0, show_name0, pwd0, pwd_Again0)

        if email0 and phone0 and name0 and show_name0 and pwd0 and pwd0 == pwd_Again0:
            models.Register.objects.create(email=email0, phone=phone0, name=name0, show_name=show_name0, password=pwd0)
            return HttpResponse('ok')
        else:
            return HttpResponse('不满足！')


def email(request):
    if request.method == 'POST':
        email0 = request.POST.get('email1')
        print(email0)
        if not email0:
            return HttpResponse('不能为空！')
        db_email = models.Register.objects.filter(email=email0)
        if db_email:
            return HttpResponse('已存在！')
        else:
            return HttpResponse('')


def phone(request):
    if request.method == 'POST':
        phone0 = request.POST.get('phone')
        print(phone0)
        if not phone0:
            return HttpResponse('不能为空！')
        db_phone0 = models.Register.objects.filter(phone=phone0)
        if db_phone0:
            return HttpResponse('已存在！')
        else:
            return HttpResponse('')


def name(request):
    if request.method == 'POST':
        name0 = request.POST.get('name')
        print(name0)
        if not name0:
            return HttpResponse('不能为空！')
        db_name0 = models.Register.objects.filter(name=name0)
        if db_name0:
            return HttpResponse('已存在！')
        else:
            return HttpResponse('')


def show_name(request):
    if request.method == 'POST':
        show_name0 = request.POST.get('show_name')
        print(show_name0)
        if not show_name0:
            return HttpResponse('不能为空！')
        db_show_name0 = models.Register.objects.filter(show_name=show_name0)
        if db_show_name0:
            return HttpResponse('已存在！')
        else:
            return HttpResponse('')


def pwd(request):
    if request.method == 'POST':
        pwd0 = request.POST.get('pwd')
        if not pwd0:
            return HttpResponse('不能为空！')
        else:
            return HttpResponse('')


def pwd_Again(request):
    if request.method == 'POST':
        pwd_Again0 = request.POST.get('pwd_Again')
        pwd0 = request.POST.get('pwd')
        print(pwd0)
        print(pwd_Again0)
        if not pwd_Again0:
            return HttpResponse('不能为空！')
        if pwd0 != pwd_Again0:
            return HttpResponse('不一致！')
        else:
            return HttpResponse('')


def homework(request):
    return render(request, 'homework.html')
