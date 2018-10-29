from django.shortcuts import render, HttpResponse, redirect, reverse
from django.contrib import auth
from crm import forms
from crm import models
from django.utils.safestring import mark_safe
from django.views import View
from django.db.models import Q
from django.http import QueryDict
from django.db import transaction
from django.conf import settings
from utils import pagination


# 展示班级
class ClassList(View):

    def get(self, request):
        # 模糊搜索
        q = self.get_search_content(['course', 'semester'])
        all_class = models.ClassList.objects.filter(q)
        # 获取路径
        query_params = self.get_query_params()
        # 分页的应用
        page = pagination.Pagination(request, len(all_class), request.GET.copy())
        return render(request, 'crm/teacher/class_list.html', {
            "all_class": all_class[page.start: page.end],
            "pagination": page.show_li,
            "query_params": query_params
        })

    def get_search_content(self, fields_list):
        query = self.request.GET.get('query', '')
        q = Q()
        q.connector = 'OR'
        for i in fields_list:
            q.children.append(Q(('{}__contains'.format(i), query)))
        return q

    def get_query_params(self):
        url = self.request.get_full_path()
        qd = QueryDict()
        qd._mutable = True
        qd['next'] = url
        query_params = qd.urlencode()
        return query_params


# 添加和编辑班级
def classes(request, edit_id=None):
    obj = models.ClassList.objects.filter(id=edit_id).first()
    title = '编辑班级' if obj else '新增班级'
    form_obj = forms.ClassForm(instance=obj)
    if request.method == 'POST':
        form_obj = forms.ClassForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            next = request.GET.get('next')
            if next:
                return redirect(next)
            else:
                return redirect(reverse('crm:class_list'))
    return render(request, 'crm/forms.html', {
        "title": title,
        "form_obj": form_obj,
    })


# 展示课程信息
class CourseList(View):
    def get(self, request, class_id):
        # 模糊查询
        q = self.get_search_content([])
        all_course = models.CourseRecord.objects.filter(q, re_class_id=class_id)
        # 获取路径
        query_params = self.get_query_params()
        # 分页
        page = pagination.Pagination(request, len(all_course), request.GET.copy())
        return render(request, 'crm/teacher/course_list.html', {
            "query_params": query_params,
            "all_course": all_course[page.start: page.end],
            'pagination': page.show_li,
            "class_id": class_id,
        })

    def get_search_content(self, fields_list):
        query = self.request.GET.get('query', '')
        q = Q()
        q.connector = 'OR'
        for i in fields_list:
            q.children.append(Q(('{}__contains'.format(i), query)))
        return q

    def get_query_params(self):
        url = self.request.get_full_path()
        qd = QueryDict()
        qd._mutable = True
        qd['next'] = url
        query_params = qd.urlencode()
        return query_params

    def post(self, request, class_id):
        action = request.POST.get('action')
        print("action", action)
        if not hasattr(self, action):
            return HttpResponse('非法操作！')
        ret = getattr(self, action)()
        print('ret', ret)
        if ret:
            return ret
        return self.get(request, class_id)

    def multi_init(self):
        # 根据当前提交的课程记录ID批量初始化学生的学校记录，也就是将这个班的各个班的人都批量导入
        course_ids = self.request.POST.getlist('id')
        print('course_ids', course_ids)
        course_obj_list = models.CourseRecord.objects.filter(id__in=course_ids)
        print('multi_init')
        # 循环将每个班级遍历  课程对象列表
        for course_obj in course_obj_list:
            # 查询当前课程记录代表的班级学生
            all_students = course_obj.re_class.customer_set.filter(status='studying')
            student_list = []
            for student in all_students:
                # 一个一个加有两种方法(sql语句一条一条执行)
                # 方法一：
                # models.StudyRecord.objects.create(course_record=course_obj)
                # 方法二：
                # obj = models.StudyRecord(course_record=course_obj, student=student)
                # obj.save()
                print('student', student)
                # 终极一条sql语句解决
                student_list.append(models.StudyRecord(course_record=course_obj, student=student))
            # 将列表中的值批量插入（一条sql语句)）
            models.StudyRecord.objects.bulk_create(student_list)


# 添加和编辑课程信息
def course(request, class_id=None, edit_id=None):
    obj = models.CourseRecord.objects.filter(id=edit_id).first() or models.CourseRecord(re_class_id=class_id,
                                                                                        teacher=request.user)
    print(1111, obj.re_class)
    print(1111, obj.re_class_id)
    form_obj = forms.CourseRecordForm(instance=obj)
    print(111111)
    title = '编辑课程' if edit_id else '新增课程'
    if request.method == 'POST':
        form_obj = forms.CourseRecordForm(request.POST, instance=obj)
        print(1, form_obj)
        if form_obj.is_valid():
            form_obj.save()
            next = request.GET.get('next')
            if next:
                return redirect(next)
            redirect(redirect(reverse('crm:course_list', args=(class_id,))))
    return render(request, 'crm/forms.html', {
        "form_obj": form_obj,
        'title': title,
    })


# 展示学习记录
from django.forms import modelformset_factory


def study_record(request, course_id):
    # 这是一个类
    FormSet = modelformset_factory(models.StudyRecord, forms.StudyRecordForm, extra=0)  # extra=0表示最后没有一行空白数据
    queryset = models.StudyRecord.objects.filter(course_record_id=course_id)
    form_set = FormSet(queryset=queryset)
    # print("form_set_get", form_set)
    if request.method == 'POST':
        form_set = FormSet(request.POST)
        # print("form_set_post", form_set)
        if form_set.is_valid():
            form_set.save()
    return render(request, 'crm/teacher/study_record_list.html', {
        "form_set": form_set,
    })
