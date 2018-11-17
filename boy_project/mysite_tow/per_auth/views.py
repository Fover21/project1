from django.shortcuts import render
from rest_framework.views import APIView
from .models import User
from rest_framework.response import Response
import uuid
from .auth import MyAuth


# Create your views here.


class LoginView(APIView):
    def post(self, request):
        name = request.data.get('name', '')
        pwd = request.data.get('pwd', '')
        user_obj = User.objects.filter(name=name, pwd=pwd).first()
        if user_obj:
            user_obj.token = uuid.uuid4()
            user_obj.save()
            # 拿到token传给前端
            return Response(user_obj.token)
        else:
            return Response('用户名或密码错误')


class TestView(APIView):
    authentication_classes = [MyAuth, ]

    def get(self, request):
        return Response('测试成功')
