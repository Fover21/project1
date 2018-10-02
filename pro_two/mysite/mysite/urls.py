"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # 程序入口
    url(r'^$', views.index),

    # 教室
    url(r'^show_class/', views.show_class),  # 展示教室
    url(r'^add_class/', views.add_class),  # 添加教室
    url(r'^del_class/', views.del_class),  # 删除教室
    url(r'^edit_class/', views.edit_class),  # 编辑教室
    url(r'^class_in_student/', views.class_in_student),  # 查询班级学生
    url(r'^class_in_teacher/', views.class_in_teacher),  # 查询班级老师

    # 学生
    url(r'^show_student/', views.show_student),  # 展示学
    url(r'^add_student/', views.add_student),  # 添加学生
    url(r'^del_student/', views.del_student),  # 删除学生
    url(r'^edit_student/', views.edit_student),  # 编辑学生

    # 老师
    url(r'^show_teacher/', views.show_teacher),  # 展示老师
    url(r'^add_teacher/', views.add_teacher),  # 添加老师
    url(r'^del_teacher/', views.del_teacher),  # 删除老师
    url(r'^edit_teacher/', views.edit_teacher),  # 编辑老师
]
