from django.shortcuts import render, redirect, HttpResponse

# Create your views here.
from django.views import View
from app02.forms import Register
from app02 import models


class Homework(View):
    form_obj = Register()

    def get(self, request):
        return render(request, 'homework.html', {'form_obj': self.form_obj})

    def post(self, request):
        self.form_obj = Register(request.POST)
        if self.form_obj.is_valid():
            print(request.POST)
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            name = request.POST.get('name')
            gender = request.POST.get('gender')
            pwd = request.POST.get('pwd')
            models.RegisterDb.objects.create(email=email, phone=phone, name=name, gender=gender, pwd=pwd)
            return HttpResponse('ok')
        print('test')
        return render(request, 'homework.html', {'form_obj': self.form_obj})