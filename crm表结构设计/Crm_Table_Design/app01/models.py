from django.db import models
from django.contrib.auth.models import BaseUserManager

# Create your models here.

'''
def __init__(self, verbose_name=None, name=None, primary_key=False,
                 max_length=None, unique=False, blank=False, null=False,
                 db_index=False, rel=None, default=NOT_PROVIDED, editable=True,
                 serialize=True, unique_for_date=None, unique_for_month=None,
                 unique_for_year=None, choices=None, help_text='', db_column=None,
                 db_tablespace=None, auto_created=False, validators=(),
                 error_messages=None):
'''


class Customer(models.Model):
    """
    客户表
    """
    # 唯一标识
    qq = models.CharField(verbose_name='qq', max_length=32, unique=True)
    name = models.CharField(verbose_name='姓名', max_length=32)
    gender = models.CharField(verbose_name='性别', choices=((1, '男'), (2, '女')), max_length=32)
    phone = models.CharField(verbose_name='手机号', max_length=32)
    #  资讯班级
    classes = models.ManyToManyField(to='Classes', verbose_name='想报名哪个班级')
    # 资讯老师、销售
    sell = models.ManyToManyField(to='UserManage', verbose_name='资讯哪个人')


class UserManage(BaseUserManager):
    """
    用户管理表
    """
    department = models.ForeignKey(to='Department', verbose_name='部门', max_length=32)


class Department(models.Model):
    """
    部门
    """
    name = models.CharField(max_length=32, verbose_name="部门名称")


class UpRecords(models.Model):
    """
    跟进记录
    """
    # 关联用户
    customer = models.ForeignKey(to='Customer', verbose_name='资讯用户')
    # 关联销售
    user_manage_sell = models.ForeignKey(to='UserManage', verbose_name='关联销售')
    status = models.CharField(verbose_name='跟进情况', max_length=32)


class Campus(models.Model):
    """
    校区表  存放校区信息
    """
    name = models.CharField(verbose_name='校区名字')
    place = models.CharField(verbose_name='校区的地点')


class Classes(models.Model):
    """
   班级课程表
    """
    course = models.CharField(verbose_name="课程名称", max_length=32)
    time = models.CharField(verbose_name="上多长时间", max_length=32)
    price = models.CharField(verbose_name='课程价格', max_length=32)
    course_start = models.DateField(verbose_name="开始上课时间")
    course_end = models.DateField(verbose_name="结束上课时间")
    # 关联课程与老师班主任与项目经理
    teacher = models.ManyToManyField(to='UserManage', verbose_name='关联课程与老师班主任与项目经理')
    # 关联在哪个校区
    campus = models.ForeignKey(to='Campus', verbose_name='关联校区')


class Apply(models.Model):
    """
    报名表
    """
    # 关联客户 这是客户转换为用户s，将信息拿来用
    customer = models.ForeignKey(to='Customer', verbose_name='用户信息')
    # 关联班级课程，知道要报什么班
    classes = models.ForeignKey(to='Classes', verbose_name='报什么班级')
    reason = models.TextField(verbose_name='报名原因')


class Payment(models.Model):
    """
    缴费记录
    """
    pay_type = models.CharField(verbose_name='缴费记录', max_length=32)
    pay_number = models.CharField(verbose_name='付款金额', max_length=32)
    pay_time = models.DateField(verbose_name='缴费时间')
    pay_course = models.CharField(verbose_name='缴费课程', max_length=32)
    # 关联缴费人信息
    customer = models.ForeignKey(to='Customer', verbose_name='客户信息')
    # 关联那个销售忽悠你来的
    sell = models.ForeignKey(to='UserManage', verbose_name='销售信息')


class CourseRecord(models.Model):
    """
    课程记录表
    """
    # 哪个班级
    classes = models.ForeignKey(to='Classes', verbose_name='哪个班的课程记录')
    course_content = models.TextField(verbose_name='课程内容')
    homework = models.TextField(verbose_name='作业内容')
    # 这个班的班主任是谁
    class_teacher = models.ForeignKey(to='UserManage', verbose_name='这个班的班主任是谁')


class StudyRecord(models.Model):
    """
    学习记录
    """
    student = models.ForeignKey('Customer', verbose_name="哪个学生")
    # 哪个班级
    classes = models.ForeignKey(to='Classes', verbose_name='哪个班的课程记录')
    attendance = models.CharField(verbose_name="出勤记录", choices=((1, '迟到'), (2, "旷课"), (3, '请假')), max_length=64)
    homework = models.CharField(verbose_name='作业情况', max_length=32)