from django.conf.urls import url
from rbac import views

urlpatterns = [

    # 角色
    url(r'^role/list/$', views.role_list, name='role_list'),
    url(r'^role/add/$', views.role, name='role_add'),
    url(r'^role/edit/(\d+)$', views.role, name='role_edit'),
    url(r'^role/del/(\d+)$', views.role_del, name='role_del'),

    # 菜单 和 权限展示在一个页面
    url(r'^menu/list/$', views.menu_list, name='menu_list'),
    # 菜单的增删改
    url(r'^menu/add/$', views.menu, name='menu_add'),
    url(r'^menu/edit/(\d+)$', views.menu, name='menu_edit'),
    url(r'^menu/del/(\d+)$', views.menu_del, name='menu_del'),
    # 权限的增删改
    url(r'^permission/add/$', views.permission, name='permission_add'),
    url(r'^permission/edit/(\d+)$', views.permission, name='permission_edit'),
    url(r'^permission/del/(\d+)$', views.permission_del, name='permission_del'),

    # 批量操作
    url(r'^multi/permissions/$', views.multi_permissions, name='multi_permissions'),

    # 分类管理权限
    url(r'^distribute/permissions/$', views.distribute_permissions, name='distribute_permissions'),

]
