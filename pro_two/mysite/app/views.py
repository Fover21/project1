from django.shortcuts import render, redirect
from app import models

# Create your views here.


# 程序入口
def index(req):
    return render(req, 'index.html')


# 教室
# 展示教室
def show_class(req):
    # 展示教室表信息
    # 先拿出教室表中信息
    class_data = models.Class.objects.all()
    return render(req, 'show_class.html', {"class_data": class_data})


# 增加教室
def add_class(req):
    # 接收到post提交的数据后
    if req.method == 'POST':
        # 先将数据拿到，再将数据存入数据库
        class_name = req.POST.get('class_name')
        class_time = req.POST.get('class_time')
        models.Class.objects.create(name=class_name, first_day=class_time)
        # 将数据存入数据库后将展示页面返回
        return redirect('/show_class/')
    # 点击添加按钮的时候弹出添加页面
    return render(req, 'add_class.html')


# 删除教室
def del_class(req):
    # 点击删除按钮
    # 获取这个按钮所在行的id
    del_id = req.GET.get('id')
    # 删除数据库中此行对应的数据，并将展示页面返回
    models.Class.objects.filter(id=del_id).delete()
    return redirect('/show_class/')


# 编辑教室
def edit_class(req):
    # 第一次点击编辑按钮的时候出现编辑页面
    # 将原先数据库中的值查出来展现到页面
    edit_id = req.GET.get('id')
    # 第二次提交的时候将获取的数据存入数据库
    if req.method == 'POST':
        # 将数据拿到存入数据库
        class_name = req.POST.get('class_name')
        class_time = req.POST.get('class_time')
        class_obj = models.Class.objects.filter(id=edit_id)[0]
        class_obj.name = class_name
        class_obj.first_day = class_time
        class_obj.save()
        # 将最终的页面展示出来
        return redirect('/show_class/')
    class_obj = models.Class.objects.filter(id=edit_id)[0]
    # 展示页面
    return render(req, 'edit_class.html', {"class_obj": class_obj})


# 学生
# 展示学生
def show_student(req):
    # 拿出学生的所有信息展示到页面
    student_data = models.Student.objects.all()
    class2teacher = models.Teacher.objects.all()
    # 将页面渲染
    return render(req, 'show_student.html', {"student_data": student_data, "class2teacher": class2teacher})


# 添加学生
def add_student(req):
    class_list = models.Class.objects.all()
    # 点击添加按钮返回添加页面
    if req.method == 'POST':
        # 将数据拿到存入数据库
        student_name = req.POST.get('student_name')
        class_name_id = req.POST.get('class_name')
        print(class_name_id)
        models.Student.objects.create(name=student_name, class_in_id=class_name_id)
        return redirect('/show_student/')
    return render(req, 'add_student.html', {"class_list": class_list})


# 删除学生
def del_student(req):
    # 获取删除行的id
    del_id = req.GET.get('id')
    # 删除数据库中内容
    models.Student.objects.filter(id=del_id).delete()
    # 展示页面
    return redirect('/show_student/')


# 编辑学生
def edit_student(req):
    # 点击编辑按钮返回编辑页面
    edit_id = req.GET.get('id')
    class_list = models.Class.objects.all()
    # 数据提交来保存并修改
    if req.method == 'POST':
        # 将数据拿到存入数据库
        student_name = req.POST.get('student_name')
        class_name_id = req.POST.get('class_name')
        student_obj = models.Student.objects.filter(id=edit_id)[0]
        student_obj.name = student_name
        student_obj.class_in_id = class_name_id
        student_obj.save()
        return redirect('/show_student/')
    # 将数据从数据库中拿出返回页面
    student = models.Student.objects.filter(id=edit_id)[0]
    return render(req, 'edit_student.html', {"class_list": class_list, "student": student})


# 老师
# 展示老师
def show_teacher(req):
    # 将教师和教室信息从数据库拿出来展示在页面
    class_list = models.Class.objects.all()
    teacher_list = models.Teacher.objects.all()
    # 展示页面
    return render(req, 'show_teacher.html', {'class_list': class_list, "teacher_list": teacher_list})


# 添加老师
def add_teacher(req):
    # 进入添加页面后点击添加按钮将数据存入数据库
    if req.method == 'POST':
        teacher_name = req.POST.get('teacher_name')
        class_name = req.POST.getlist('class_name')
        # 将数据存入数据库
        teacher_obj = models.Teacher.objects.create(name=teacher_name)
        teacher_obj.teacher2class.set(class_name)
        # 返回页面
        return redirect('/show_teacher/')
    # 点击添加按钮将教室名字展示出来供选择
    # 拿出所有教室
    class_list = models.Class.objects.all()
    return render(req, 'add_teacher.html', {'class_list': class_list})


# 删除老师
def del_teacher(req):
    # 拿到删除行的id
    del_id = req.GET.get('id')
    # 将数据库中这行数据删除
    models.Teacher.objects.filter(id=del_id).delete()
    # 返回删除后页面
    return redirect('/show_teacher/')


# 编辑老师
def edit_teacher(req):
    # 先将老师这行数据展示
    edit_id = req.GET.get('id')
    # 拿到此行对应的数据
    teacher_obj = models.Teacher.objects.filter(id=edit_id)[0]
    # 拿到所有教室
    class_list = models.Class.objects.all()
    # 将编辑好的数据发来
    if req.method == "POST":
        # 拿到发来的数据
        teacher_name = req.POST.get('teacher_name')
        class_name = req.POST.getlist('class_name')
        # 存入数据库
        teacher_obj.name = teacher_name
        teacher_obj.save()
        teacher_obj.teacher2class.set(class_name)
        # 返回展示页面
        return redirect('/show_teacher/')
    # 返回展示页面
    return render(req, 'edit_teacher.html', {'teacher_obj': teacher_obj, "class_list": class_list})
