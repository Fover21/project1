from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation


# Create your models here.

class Food(models.Model):
    """
    id  name
    1   酱香饼
    2   鸡蛋饼
    3   水煎包
    """
    name = models.CharField(max_length=32)
    # 不生成字段只用于反向查询
    coupons = GenericRelation(to='Coupon')


class Fruit(models.Model):
    """
    id  name
    1   红心蜜柚
    2   黑美人西瓜
    """
    name = models.CharField(max_length=32)
    coupons = GenericRelation(to='Coupon')


class Coupon(models.Model):
    """
    id  title           food_id     fruit_id
    1   酱香饼买一送一      1           null
    2   黑美人西瓜2折      null          2

    id  title           table_id    object_id
    1   酱香饼买一送一         1           1
    2   黑美人西瓜2折         2           2
    """
    title = models.CharField(max_length=32)
    # 一
    # food = models.ForeignKey(to='Food')
    # fruit = models.ForeignKey(to='Fruit')
    # 二
    # table = models.ForeignKey(to="MyTables")
    # object_id = models.IntegerField()
    # 三 Django字典的Content-type表
    content_type = models.ForeignKey(to=ContentType)
    object_id = models.IntegerField()
    # 不会生成字段 只用于关联到对象
    content_object = GenericForeignKey("content_type", "object_id")

# class MyTables(models.Model):
#     """
#     id  app_name                        table_name
#     1   content_type_model                food
#     2   content_type_model                fruit
#     """
#     app_name = models.CharField(max_length=32)
#     table_name = models.CharField(max_length=32)
