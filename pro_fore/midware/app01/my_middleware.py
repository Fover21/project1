# __author: ward
# data: 2018/10/15


from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, HttpResponse, redirect
import time


# ---------practice----------
# class MD1(MiddlewareMixin):
#
#     def process_request(self, request):
#         print('process_request req1', request)
#
#
# class MD2(MiddlewareMixin):
#
#     def process_request(self, request):
#         print('process_request req2', request)


# ------------homework-----------
class MDHomework(MiddlewareMixin):
    black_url = ['/black/']
    white_url = ['/login/']
    ip_set = set()
    time_list = []

    def process_request(self, request):
        next_url = request.path_info
        ip = request.META['REMOTE_ADDR']
        print(ip)
        self.ip_set.add(ip)
        print(self.ip_set)
        print(self.time_list)

        if next_url in self.white_url or request.session.get('is_login') == '1':
            return None
        elif next_url in self.black_url:
            return HttpResponse('黑名单！')
        else:
            return redirect('/login/?next={}'.format(next_url))
