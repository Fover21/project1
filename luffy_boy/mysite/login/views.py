from rest_framework.views import APIView
from .serializers import AccountSerializer
from rest_framework.response import Response
from utils.base_response import BaseResponse
from course.models import Account
import uuid


# Create your views here.

class RegisterView(APIView):
    # 用户注册要传用户名和密码  新增数据
    def post(self, request):
        # 获取用户名和密码
        # 拿序列化器做校验
        ser_obj = AccountSerializer(data=request.data)
        if ser_obj.is_valid():
            ser_obj.save()
            return Response('注册成功！')
        # 返回新增的数据  用户名 看要什么
        return Response(ser_obj.errors)


class LoginView(APIView):
    def post(self, request):
        ret = BaseResponse()
        # 获取用户名和密码

        username = request.data.get('username')
        if not username:
            ret.code = 1010
            ret.error = '用户名不能为空'
        pwd = request.data.get('pwd')
        if not pwd:
            ret.code = 1011
            ret.error = '密码不能为空'
            return Response(ret.dict)
        # 判断是否有这个用户对象
        try:
            # 从数据库拿出账户密码进行对比
            user_obj = Account.objects.filter(username=username, pwd=pwd).first()
            if not user_obj:
                ret.code = 1012
                ret.error = '用户名或密码错误'
                return Response(ret.dict)
            # 生成token
            user_obj.token = uuid.uuid4()
            user_obj.save()
            ret.data = '登录成功！'
        except Exception as e:
            print(e)
            ret.code = 1013
            ret.error = '登录失败'
        return Response(ret.dict)
