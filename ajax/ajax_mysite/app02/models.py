from django.db import models

# Create your models here.


class Register(models.Model):
    email = models.EmailField()
    phone = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    show_name = models.CharField(max_length=32)
    password = models.CharField(max_length=32)