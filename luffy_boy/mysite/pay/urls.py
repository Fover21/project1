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
from .views import ShoppingCarView, AccountView, PaymentView


urlpatterns = [
    # 购物车接口
    url(r'^shopping_car', ShoppingCarView.as_view()),
    # 结算接口
    url(r'^account', AccountView.as_view()),
    # 支付接口
    url(r'^payment', PaymentView.as_view()),
]
