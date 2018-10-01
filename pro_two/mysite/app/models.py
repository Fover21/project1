from django.db import models


# Create your models here.

# 教室表
class Class(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)
    first_day = models.DateField()


# 学生表
class Student(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)
    class_in = models.ForeignKey(to='Class', on_delete=models.CASCADE)


# 教师表
class Teacher(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)
    teacher2class = models.ManyToManyField(to='Class')
    teacher2student = models.ManyToManyField(to='Student')


