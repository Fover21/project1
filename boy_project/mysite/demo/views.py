from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
from demo import models
import json

import rest_framework
from django.core import serializers


def tryagain(requset):
    return HttpResponse('ok')

# Create your views here.
# book_list = [
#     {
#         "id": 1,
#         "title": 'xx',
#         ...
#     }
# ]


class BookView(View):
    def get(self, request):
        book_queryset = models.Book.objects.all().values("id", 'title')
        book_list = list(book_queryset)
        # 方式一
        # ret = json.dumps(book_list, ensure_ascii=False)
        # return HttpResponse(ret)
        # 方式二 Django的序列化
        # book_list_obj = models.Book.objects.all()
        # ret = serializers.serialize('json', book_list_obj, ensure_ascii=False)
        # return HttpResponse(ret)
        # 方式三
        return JsonResponse(book_list, safe=False, json_dumps_params={"ensure_ascii": False})


