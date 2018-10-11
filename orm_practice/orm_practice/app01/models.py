from django.db import models


# 自定义一个char类型字段：
class MyCharField(models.Field):
    """
    自定义的char类型的字段类
    """

    def __init__(self, max_length, *args, **kwargs):
        self.max_length = max_length
        super(MyCharField, self).__init__(max_length=max_length, *args, **kwargs)

    def db_type(self, connection):
        """
        限定生成数据库表的字段类型为char，长度为max_length指定的值
        """
        return 'char(%s)' % self.max_length


class Person(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)
    age = models.IntegerField()
    birth = models.DateField(auto_now_add=True)  # 添加的时候的时间  auto_now 修改的时候的时间 default 三者互斥
    phone = MyCharField(max_length=11)

    def __str__(self):
        return '%s-%s' % (self.id, self.name)


# 班级表
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
    teacher2student = models.ManyToManyField(to='Student')



