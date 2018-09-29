from django.db import models


# Create your models here.

class Press(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32)
    # 一个出版社可以出版多本书，为书设置出版社外键
    # to = 为哪个表设置外键（Django1.x on_delete默认有，2.x之后需要手动加）
    press = models.ForeignKey(to='Press', on_delete=models.CASCADE)