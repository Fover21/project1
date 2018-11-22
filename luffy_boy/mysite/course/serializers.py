# __author: ward
# data: 2018/11/20

from rest_framework import serializers
from . import models


class CategorySerializer(serializers.ModelSerializer):
    """
    课程分类序列化器
    """

    class Meta:
        model = models.Category
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    """
    课程序列化器
    """
    level = serializers.CharField(source='get_level_display')
    price = serializers.SerializerMethodField()
    course_img = serializers.SerializerMethodField()

    def get_course_img(self, obj):
        return "http://127.0.0.1:8000/media/" + str(obj.course_img)

    def get_price(self, obj):
        price_policy_obj = obj.price_policy.all().order_by("price").first()
        return price_policy_obj.price

    class Meta:
        model = models.Course
        fields = ['id', 'title', 'course_img', 'brief', 'level', 'study_num', 'is_free', 'price']


class CourseDetailSerializer(serializers.ModelSerializer):
    """
    课程详细信息序列化器
    """
    # 头部显示的公共字段
    title = serializers.SerializerMethodField()
    level = serializers.SerializerMethodField()
    study_num = serializers.SerializerMethodField()

    # 推荐课程
    recommend_courses = serializers.SerializerMethodField()
    # 教师介绍
    teachers = serializers.SerializerMethodField()
    # 大纲表
    outline = serializers.SerializerMethodField()
    # 价格策略表
    price_policy = serializers.SerializerMethodField()

    def get_recommend_courses(self, obj):
        return [{"id": item.id, "title": item.title} for item in obj.recommend_courses.all()]

    def get_teachers(self, obj):
        return [{"id": item.id, 'name': item.name, "brief": item.brief} for item in obj.teachers.all()]

    def get_outline(self, obj):
        return [{'id': item.id, 'title': item.title, 'content': item.content} for item in
                obj.course_outline.all().order_by('order')]

    # 价格字段需要跨表，从本身的one2one到course再到价格策略表
    def get_price_policy(self, obj):
        return [{'id': item.id, 'valid_period': item.get_valid_period_display()} for item in
                obj.course.price_policy.all().order_by('price')]

    # 头部公用的字段
    def get_title(self, obj):
        return obj.course.title

    def get_level(self, obj):
        return obj.course.get_level_display()

    def get_study_num(self, obj):
        return obj.course.study_num

    class Meta:
        model = models.CourseDetail
        exclude = ['course']


class CourseChapterSerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField()
    section_title = serializers.SerializerMethodField()

    def get_course(self, obj):
        return obj.course.title

    def get_section_title(self, obj):
        return [{'id': item.id, 'section_title': item.title} for item in
                obj.course_sections.all().order_by('section_order')]

    class Meta:
        model = models.CourseChapter
        exclude = ['chapter']
