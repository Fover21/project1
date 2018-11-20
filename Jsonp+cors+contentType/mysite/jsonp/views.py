from django.shortcuts import render, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.

class CorsDemoView(APIView):
    def get(self, request):
        # return HttpResponse('ok')
        # return HttpResponse('handlerResponse("ok")')
        callback = request.query_params.get("callback", "")
        ret = callback + "(" + "'success'" + ")"
        return HttpResponse(ret)

    def post(self, request):
        return HttpResponse('POST')

    def put(self, request):
        return HttpResponse('PUT')
