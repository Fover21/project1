"""pro_one URL Configuration

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
from app_one import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # 文件上传
    url(r'^index/', views.index),


    # 出版社
    url(r'^$', views.index),  # 主页信息
    url(r'^press_list/', views.press_list),  # 展示出版社信息
    url(r'^add_press/', views.add_press),  # 添加出版社信息
    url(r'^del_press/', views.del_press),  # 删除出版社信息
    url(r'^edit_press/', views.edit_press),  # 编辑出版社信息


    # 书
    url(r'^book_list/', views.book_list),  # 展示书籍信息
    url(r'^add_book/', views.add_book),  # 添加书籍信息
    url(r'^del_book/', views.del_book),  # 删除书籍信息
    url(r'^edit_book/', views.edit_book),  # 编辑书籍信息


    # 作者
    url(r'^author_list/', views.author_list),  # 展示作者信息
    url(r'^add_author/', views.add_author),  # 添加作者信息
    url(r'^del_author/', views.del_author),  # 删除作者信息
    url(r'^edit_author/', views.edit_author),  # 编辑作者信息

]
