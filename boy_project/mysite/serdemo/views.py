from demo import models
from rest_framework.views import APIView
from rest_framework.response import Response
from serdemo import serializers
from rest_framework.viewsets import ViewSetMixin

from rest_framework import views  # APIView
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import mixins
from .pagination import MyPaginator, MyCursorPagination, MyLimitOffset


# queryset不同  序列化器不同
# def get:pass
# def post:pass


class GenericAPIView(APIView):
    queryset = None
    serializer_class = None

    def get_queryset(self):
        return self.queryset.all()

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)


class ListModelMixin(object):
    def list(self, request):
        queryset = self.get_queryset()
        ser_obj = self.get_serializer(queryset, many=True)
        return Response(ser_obj.data)


class CreateModelMixin(object):
    def create(self, request):
        ser_obj = self.get_serializer(data=request.data)
        if ser_obj.is_valid():
            ser_obj.save()
            return Response(ser_obj.data)
        return Response(ser_obj.errors)


class RetrieveModelMixin(object):
    def retrieve(self, request, id):
        book_obj = self.get_queryset().filter(id=id).first()
        ser_obj = serializers.BookSerializer(book_obj)
        return Response(ser_obj.data)


class UpdateModelMixin(object):
    def update(self, request, id):
        book_obj = self.get_queryset().filter(id=id).first()
        ser_obj = self.get_serializer(instance=book_obj, data=request.data, partial=True)
        if ser_obj.is_valid():
            ser_obj.save()
            return Response(ser_obj.data)
        return Response(ser_obj.errors)


class DestroyModelMixin(object):
    def destroy(self, request, id):
        book_obj = self.get_queryset().filter(id=id).first()
        if not book_obj:
            return Response("删除的对象不存在")
        book_obj.delete()
        return Response("")


class ListCreateAPIView(GenericAPIView, ListModelMixin, CreateModelMixin):
    pass


class RetrieveUpdateDestroyAPIView(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    pass


class ModelViewSet(ViewSetMixin, ListModelMixin, RetrieveUpdateDestroyAPIView):
    pass


# get post
# 封装一
# class BookView(GenericAPIView, ListModelMixin, CreateModelMixin):
#     queryset = models.Book.objects.all()
#     serializer_class = serializers.BookSerializer
#
#     def get(self, request):
#         return self.list(request)
#
#     def post(self, request):
#         return self.create(request)


# get put delete
# 封装一
# class BookEditView(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
#     queryset = models.Book.objects.all()
#     serializer_class = serializers.BookSerializer
#
#     def get(self, request, id):
#         return self.retrieve(request, id)
#
#     def put(self, request, id):
#         return self.update(request, id)
#
#     def delete(self, request, id):
#         return self.destroy(request, id)


# # 分装二
# class BookView(ListCreateAPIView):
#     queryset = models.Book.objects.all()
#     serializer_class = serializers.BookSerializer
#
#     def get(self, request):
#         return self.list(request)
#
#     def post(self, request):
#         return self.create(request)
#
#
# # 封装二
# class BookEditView(RetrieveUpdateDestroyAPIView):
#     queryset = models.Book.objects.all()
#     serializer_class = serializers.BookSerializer
#
#     def get(self, request, id):
#         return self.retrieve(request, id)
#
#     def put(self, request, id):
#         return self.update(request, id)
#
#     def delete(self, request, id):
#         return self.destroy(request, id)


# 分装三  BookModelView
class BookModelView(viewsets.ModelViewSet):  # 只需要在路由中指定字典就可以
    queryset = models.Book.objects.all()
    serializer_class = serializers.BookSerializer
    # 分页一
    pagination_class = MyPaginator
    # 分页二
    # pagination_class = MyLimitOffset
    # 分页三
    # pagination_class = MyCursorPagination


# class BookView(APIView):
#
#     def get(self, request):
#         book_queryset = models.Book.objects.all()
#         ser_obj = serializers.BookSerializer(book_queryset, many=True)
#         return Response(ser_obj.data)
#
#     def post(self, request):
#         # 确定数据类型已经数据结构
#         # 对妹子传来的数据进行校验
#         book_obj = request.data
#         ser_obj = serializers.BookSerializer(data=book_obj)
#         if ser_obj.is_valid():
#             ser_obj.save()
#             # 校验通过的数据
#             return Response(ser_obj.validated_data)
#         return Response(ser_obj.errors)


# class BookEditView(APIView):
#     def get(self, request, id):
#         book_obj = models.Book.objects.filter(id=id).first()
#         ser_obj = serializers.BookSerializer(book_obj)
#         return Response(ser_obj.data)
#
#     def put(self, request, id):
#         book_obj = models.Book.objects.filter(id=id).first()
#         # partial=True 代表的是可以改部分数据
#         ser_obj = serializers.BookSerializer(instance=book_obj, data=request.data, partial=True)
#         if ser_obj.is_valid():
#             ser_obj.save()
#             return Response(ser_obj.validated_data)
#         return Response(ser_obj.errors)
#
#     def delete(self, request, id):
#         book_obj = models.Book.objects.filter(id=id).first()
#         if not book_obj:
#             return Response('删除对象不存在')
#         book_obj.delete()
#         return Response("")


class PageBookView(APIView):
    def get(self, request):
        queryset = models.Book.objects.all()
        # 先实例化分页器对象
        # page_obj = MyPaginator()
        # page_obj = MyLimitOffset()
        page_obj = MyCursorPagination()
        # 用自己的分页器调用分页方法进行分页
        page_data = page_obj.paginate_queryset(queryset, request)
        # 序列化分页好的数据
        ser_obj = serializers.BookSerializer(page_data, many=True)
        # 给响应添加上一页下一页的链接
        return page_obj.get_paginated_response(ser_obj.data)


