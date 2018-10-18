"""ajax_mysite URL Configuration

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
from app02 import views as v2
urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^login/', views.login),

    url(r'^index/', views.index),
    url(r'^calc/', views.calc),

    # 上传
    url(r'^upload/', views.upload),

    # 注册的ajax
    url(r'^homework/', v2.homework),
    url(r'^email/', v2.email,),
    url(r'^phone/', v2.phone),
    url(r'^name/', v2.name),
    url(r'^show_name/', v2.show_name),
    url(r'^pwd/', v2.pwd),
    url(r'^pwd_Again/', v2.pwd_Again),
    # 提交
    url(r'^register/', v2.register),


    # test
    url(r'^tt/', views.tt, name='uu'),

]
