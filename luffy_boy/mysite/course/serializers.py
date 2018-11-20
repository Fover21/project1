# __author: ward
# data: 2018/11/20

from rest_framework import serializers
from . import models


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    level = serializers.CharField(source='get_level_display')
    price = serializers.SerializerMethodField()

    def get_price(self, obj):
        price_policy_obj = obj.price_policy.all().order_by("price").first()
        return price_policy_obj.price

    class Meta:
        model = models.Course
        fields = ['id', 'title', 'course_img', 'brief', 'level', 'study_num', 'is_free', 'price']