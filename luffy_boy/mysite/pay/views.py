from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from utils.authentication import MyAuth


# Create your views here.

class ShoppingCarView(APIView):
    authentication_classes = [MyAuth, ]

    def post(self, request):
        return Response('ok')
