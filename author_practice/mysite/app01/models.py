from django.db import models

# Create your models here.


# class RegisterDb(models.Model):
#     email = models.CharField(max_length=32)
#     phone = models.CharField(max_length=32)
#     name = models.CharField(max_length=32)
#     gender = models.CharField(max_length=32, choices=((1, '男'), (2, "女")))
#     pwd = models.CharField(max_length=32)


from django.contrib.auth.models import User, AbstractUser


# 扩展表
class UserInfo(AbstractUser):
    phone = models.CharField(max_length=11)