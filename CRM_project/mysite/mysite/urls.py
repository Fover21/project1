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
from django.conf.urls import url, include
from django.contrib import admin
from crm.views import consultant

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # 登录
    url(r'^login/', consultant.login, name='login'),
    # 注销
    url(r'^logout/', consultant.login, name='logout'),

    # 注册
    url(r'^register/', consultant.register),
    # 展示客户信息
    url(r'^crm/', include('crm.urls', namespace='crm')),


    # 测试分页
    url(r'^user_list/', consultant.user_list),
    # 练习分页
    url(r'^practice_pagination/', consultant.practice_pagination),
]
