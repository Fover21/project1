from demo import models
from rest_framework.views import APIView
from rest_framework.response import Response
from serdemo import serializers
from rest_framework.viewsets import ViewSetMixin


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


class RetrieveeModelMixin(object):
    def retrieve(self, request, id):
        book_obj = self.get_queryset().filter(id=id).first()
        ser_obj = serializers.BookSerializer(book_obj)
        return Response(ser_obj.data)


class UpdateModeMixin(object):
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


# get post
class BookView(GenericAPIView, ListModelMixin, CreateModelMixin):
    queryset = models.Book.objects.all()
    serializer_class = serializers.BookSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


# get put delete
class BookEditView(GenericAPIView, RetrieveeModelMixin, UpdateModeMixin, DestroyModelMixin):
    queryset = models.Book.objects.all()
    serializer_class = serializers.BookSerializer

    def get(self, request, id):
        return self.retrieve(request, id)

    def put(self, request, id):
        return self.update(request, id)

    def delete(self, request, id):
        return self.destroy(request, id)

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
