from rest_framework.views import APIView
from .models import User
from rest_framework.response import Response
import uuid
from .auth import MyAuth
from .permission import MyPermission
from .throttle import MyThrottle, DRDThrottle
from rest_framework import versioning
from .version import MyVersion


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


class TestPermission(APIView):
    authentication_classes = [MyAuth, ]
    permission_classes = [MyPermission, ]
    throttle_classes = [MyThrottle, ]

    def get(self, request):
        return Response('VIP能看的视频')


class TestVersion(APIView):

    def get(self, request):
        print(request.version)
        print(request.versioning_scheme)
        # 根据版本号处理不同业务逻辑
        if request.version == "v2":
            return Response("这是v2的版本返回信息")
        return Response("这是v1的版本返回信息")


