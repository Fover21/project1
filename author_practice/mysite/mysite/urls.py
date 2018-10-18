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
from app01 import views
from app02 import views as v
urlpatterns = [
    url(r'^admin/', admin.site.urls),


    url(r'^login/', views.login),
    url(r'^index/', views.index),
    url(r'^reg/', views.Homework.as_view()),

    url(r'^login1/', v.MyLogin.as_view()),
    url(r'^index1/', v.MyIndex.as_view()),
    url(r'^reg1/', v.MyReg.as_view()),
    url(r'^change_pwd/', v.MyPwd.as_view()),



]
