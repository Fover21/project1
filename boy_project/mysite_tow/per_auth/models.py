from django.db import models


# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=32)
    pwd = models.CharField(max_length=32)
    # 验证随机码记录登录状态
    token = models.UUIDField(null=True, blank=True)
