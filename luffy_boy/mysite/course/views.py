from rest_framework.views import APIView
from rest_framework.response import Response
from . import models
from . import serializers


# Create your views here.

class CourseCategoryView(APIView):
    """
    课程分类
    """
    def get(self, request):
        # 从数据库中拿出所有的分类
        queryset = models.Category.objects.all()
        # 序列化所有的分类
        ser_obj = serializers.CategorySerializer(queryset, many=True)
        # 返回序列化的数据
        return Response(ser_obj.data)


class CourseView(APIView):
    """
    课程表
    """
    # /xxxxx/xxxx?category_id=0
    def get(self, request):
        # 判断是否有category_id
        category_id = request.query_params.get('category_id', 0)
        category_id = int(category_id)
        # 获取响应的数据类型
        if not category_id:
            queryset = models.Course.objects.all().order_by("order")
        else:
            queryset = models.Course.objects.filter(category_id=category_id).order_by("order")
        # 序列化数据
        ser_obj = serializers.CourseSerializer(queryset, many=True)
        # 返回序列化好的数据
        return Response(ser_obj.data)


class CourseDetailView(APIView):
    """
    课程详情概述
    """
    def get(self, request, id):
        # 获取这个课程id找到课程详情对象
        course_detail_obj = models.CourseDetail.objects.filter(course_id=id).first()
        # 序列化这个课程详情对象
        ser_obj = serializers.CourseDetailSerializer(course_detail_obj)
        # 返回序列化数据
        return Response(ser_obj.data)


class CourseChapterView(APIView):
    """
    课程章节
    """
    def get(self, request):
        # 获取所有章节对象
        course_chapter_obj = models.CourseChapter.objects.all()
        ser_obj = serializers.CourseChapterSerializer(course_chapter_obj, many=True)
        return Response(ser_obj.data)