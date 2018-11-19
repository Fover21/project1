# __author: busensei
# data: 2018/11/17
import time
from rest_framework.throttling import SimpleRateThrottle

VISIT_RECORD = {}


class MyThrottle(object):
    """
    一分钟访问五次（可以设置为配置信息）
    """

    def __init__(self):
        self.history = None

    def allow_request(self, request, view):
        # 获取用户的ip地址
        ip = request.META.get('REMOTE_ADDR', '')
        # self.key = self.get_catch_key()
        # self.cache.get(self.key, [])
        # 构建访问记录
        if ip not in VISIT_RECORD:
            VISIT_RECORD[ip] = [time.time(), ]
        else:
            history = VISIT_RECORD[ip]
            self.history = history
            history.insert(0, time.time())
            # 确保列表的时间是允许范围内的
            while self.history[0] - self.history[-1] > 60:
                self.history.pop()
            # 判断列表的长度
            if not len(self.history) <= 5:
                return False
        return True

    # 等待信息
    # [最近时间，   最老时间]
    def wait(self):
        return 60 - (self.history[0] - self.history[-1])


class DRDThrottle(SimpleRateThrottle):

    scope = "WD"

    def get_cache_key(self, request, view):
        """拿IP地址"""
        return self.get_ident(request)
