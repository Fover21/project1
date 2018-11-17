# __author: ward
# data: 2018/11/17
from .models import User
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import BaseAuthentication


class MyAuth(BaseAuthentication):
    def authenticate(self, request):
        # 认证逻辑
        # 拿到前端传来的token
        # 判断token是否存在
        token = request.query_params.get('token', '')
        if not token:
            raise AuthenticationFailed('没有token')
        user_obj = User.objects.filter(token=token).first()
        if not user_obj:
            raise AuthenticationFailed('token不合法')
        # request.user   request.auth
        return (user_obj, token)
