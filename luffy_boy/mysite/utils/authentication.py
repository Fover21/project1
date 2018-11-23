# __author: busensei
# data: 2018/11/22
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from course.models import Account
import datetime  # datatime 不好做运算，因为时区的原因
from django.utils.timezone import now  # 这个当前时间符合Django配置的当地时间


class MyAuth(BaseAuthentication):
    def authenticate(self, request):
        if request.method == 'OPTIONS':
            return None
        # 认证的逻辑
        # 拿到前端的token
        token = request.META.get('HTTP_AUTHENTICATE', '')
        if not token:
            raise AuthenticationFailed({
                "code": 1021,
                "error": '没有携带token'
            })
        user_obj = Account.objects.filter(token=token).first()
        if not user_obj:
            raise AuthenticationFailed({
                "code": 1021,
                "error": 'token不合法'
            })
        # token是否过期
        old_time = user_obj.create_token_time
        now_time = now()
        if (now_time - old_time).days > 7:
            raise AuthenticationFailed({
                "code": 1022,
                "error": 'token过期重新登录'
            })
        return user_obj, token
