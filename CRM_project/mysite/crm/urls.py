
from django.conf.urls import url
from crm import views

urlpatterns = [
    # 展示客户信息
    url(r'^customer_list/', views.customer_list, name='customer'),
]
