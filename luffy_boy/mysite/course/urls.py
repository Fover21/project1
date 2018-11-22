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
from .views import CourseCategoryView, CourseView, CourseDetailView, CourseChapterView

urlpatterns = [
    # 课程分类接口    http://127.0.0.1:8000/api/course/category
    url(r'^category$', CourseCategoryView.as_view()),
    # 课程接口  http://127.0.0.1:8000/api/course/   http://127.0.0.1:8000/api/course/?catagory_id=x
    url(r'^$', CourseView.as_view()),
    # 课程详情接口    http://127.0.0.1:8000/api/course/detail/x
    url(r'^detail/(?P<id>\d+)', CourseDetailView.as_view()),
    # 课程章节接口
    url(r'^course_chapter', CourseChapterView.as_view()),



]
