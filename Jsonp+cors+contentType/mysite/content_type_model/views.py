from django.shortcuts import render, HttpResponse
from rest_framework.views import APIView
from .models import Fruit, Food, Coupon
from django.contrib.contenttypes.models import ContentType


# Create your views here.

class TestDemo(APIView):
    def get(self, request):
        # 找到表id以及表对象
        content_type_obj = ContentType.objects.filter(app_label='content_type_model', model='food').first()
        print('content_type_obj及类型', content_type_obj, type(content_type_obj))
        model_class = content_type_obj.model_class()
        print('model_class', model_class)
        print('content_type_obj.id', content_type_obj.id)

        # contentType方法
        # 给饼创建优惠卷
        # food_obj = Food.objects.filter(id=1).first()
        # Coupon.objects.create(title='饼买一送一', content_object=food_obj)

        # 普通方法
        # 给西瓜加优惠卷
        # fuirt_obj = Food.objects.filter(id=1).first()
        # Coupon.objects.create(title='西瓜1折', content_type_id=9, object_id=1)

        # 查询优惠卷绑定对象 - 正向查询
        coupon_obj = Coupon.objects.filter(id=1).first()
        print('coupon_obj的属性', coupon_obj.content_object.name)
        # 查询某个对象的优惠券 - 反向查询
        food_obj = Food.objects.filter(id=1).first()
        print('food_obj', food_obj.coupons.all())
        return HttpResponse('ok')
