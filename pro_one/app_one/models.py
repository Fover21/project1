from django.db import models


# Create your models here.

# 出版社
class Press(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


# 书
class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32)
    # 一个出版社可以出版多本书，为书设置出版社外键
    # to = 为哪个表设置外键（Django1.x on_delete默认有，2.x之后需要手动加）
    press = models.ForeignKey(to='Press', on_delete=models.CASCADE)


# 作者
class Author(models.Model):
    id = models.AutoField(primary_key=id)
    name = models.CharField(max_length=32)
    # 作者与书籍是多对多的关系(ORM会自动创建第三张表)
    books = models.ManyToManyField(to='Book')