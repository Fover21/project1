from rest_framework.views import APIView
from rest_framework.response import Response
from . import models
from . import serializers


# Create your views here.

class CourseCategoryView(APIView):
    def get(self, request):
        # 从数据库中拿出所有的分类
        queryset = models.Category.objects.all()
        # 序列化所有的分类
        ser_obj = serializers.CategorySerializer(queryset, many=True)
        # 返回序列化的数据
        return Response(ser_obj.data)


class CourseView(APIView):
    def get(self, request):
        # 判断是否有category_id
        category_id = request.query_params.get('category_id', "")
        # 获取响应的数据类型
        if not category_id:
            queryset = models.Course.objects.all().order_by("order")
        else:
            queryset = models.Course.objects.filter(category_id=category_id).order_by("order")
        # 序列化数据
        ser_obj = serializers.CourseSerializer(queryset, many=True)
        # 返回序列化好的数据
        return Response(ser_obj.data)