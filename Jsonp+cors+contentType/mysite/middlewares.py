# __author: busensei
# data: 2018/11/20

from django.utils.deprecation import MiddlewareMixin


class MyCors(MiddlewareMixin):
    def process_response(self, request, response):
        # 解决简单请求
        response["Access-Control-Allow-Origin"] = "*"
        # 解决复杂请求
        if request.method == "OPTIONS":
            response["Access-Control-Allow-Headers"] = "Content-Type"
            response["Access-Control-Allow-Methods"] = "DELETE, PUT, POST"
        return response
