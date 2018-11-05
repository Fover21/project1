from django.shortcuts import render, reverse, redirect, HttpResponse
from rbac import models
from rbac import forms
from django.db.models import Q
from rbac.server.routes import get_all_url_dict
from django.forms import modelformset_factory
from django.forms import formset_factory


# Create your views here.


# 角色列表
def role_list(request):
    all_roles = models.Role.objects.all()
    return render(request, 'rbac/role_list.html', {
        "all_roles": all_roles
    })


# 角色的添加和编辑
def role(request, edit_id=None):
    obj = models.Role.objects.filter(id=edit_id).first()
    title = '添加角色' if not edit_id else '编辑角色'
    form_obj = forms.RoleForm(instance=obj)
    if request.method == 'POST':
        form_obj = forms.RoleForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('rbac:role_list'))
    return render(request, 'rbac/form.html', {
        "form_obj": form_obj,
        "title": title
    })


# 角色的删除
def role_del(request, del_id):
    models.Role.objects.filter(id=del_id).delete()
    return redirect(reverse('rbac:role_list'))


# 菜单和权限的展示
# 点击每一个菜单出现对应的权限信息
def menu_list(request):
    all_menu = models.Menu.objects.all()
    # 拿到菜单对应的菜单id
    mid = request.GET.get('mid')
    # 如果拿到菜单id代表着有子权限
    if mid:
        # 从子权限出发 拿到 父权限对应的菜单id对应的权限  或者  菜单对应的权限（也就是二级菜单） 因为自己关联自己（从父亲和儿子两方面出发）
        permission_query = models.Permission.objects.filter(Q(menu_id=mid) | Q(parent__menu_id=mid))
    # 如果没有菜单id则输出所有的权限信息
    else:
        permission_query = models.Permission.objects.all()
    # 拿到查询出的权限对应的信息
    all_permission = permission_query.values('id', 'url', 'title', 'name', 'menu_id', 'parent_id', 'menu__title')
    all_permission_dict = {}
    for item in all_permission:
        menu_id = item.get('menu_id')
        # 找到有菜单id的权限，将其存入字典，键为权限的id
        if menu_id:
            all_permission_dict[item['id']] = item
            # 可以改都是引用
            # 得到所有有菜单的权限后，将每一个权限都设置一个children键值对，用来存储子权限信息
            item['children'] = []
    for item in all_permission:
        pid = item.get('parent_id')
        # 如果有父id代表的是子权限
        if pid:
            # 如果是子权限，就将子权限的信息存入多上一步做的处理（有菜单的父权限）children中
            all_permission_dict[pid]['children'].append(item)
    return render(request, 'rbac/menu_list.html', {
        "mid": mid,
        "all_menu": all_menu,
        "all_permission_dict": all_permission_dict,
    })


# 菜单的添加和编辑
def menu(request, edit_id=None):
    obj = models.Menu.objects.filter(id=edit_id).first()
    title = '添加菜单' if not edit_id else '编辑菜单'
    form_obj = forms.MenuForm(instance=obj)
    if request.method == 'POST':
        form_obj = forms.MenuForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('rbac:menu_list'))
    return render(request, 'rbac/form.html', {
        "form_obj": form_obj,
        "title": title
    })


# 菜单的删除
def menu_del(request, del_id):
    models.Menu.objects.filter(id=del_id).delete()
    return redirect(reverse('rbac:menu_list'))


# 权限的添加和编辑
def permission(request, edit_id=None):
    obj = models.Permission.objects.filter(id=edit_id).first()
    title = '添加权限' if not edit_id else '编辑权限'
    form_obj = forms.PermissionForm(instance=obj)
    if request.method == 'POST':
        form_obj = forms.PermissionForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('rbac:menu_list'))
    return render(request, 'rbac/form.html', {
        "form_obj": form_obj,
        "title": title
    })


# 权限的删除
def permission_del(request, del_id):
    models.Permission.objects.filter(id=del_id).delete()
    return redirect(reverse('rbac:menu_list'))


# 批量操作
def multi_permissions(request):
    """
    批量操作权限
    :param request:
    :return:
    """
    post_type = request.GET.get('type')

    # 更新和编辑用的
    FormSet = modelformset_factory(models.Permission, forms.MultiPermissionForm, extra=0)
    # 增加用的
    AddFormSet = formset_factory(forms.MultiPermissionForm, extra=0)

    permissions = models.Permission.objects.all()

    # 获取路由系统中的所有URL
    router_dict = get_all_url_dict(ignore_namespace_list=['admin', ])

    # 数据库中的所有权限的别名
    permissions_name_set = set([i.name for i in permissions])

    # 路由系统中的所有的权限的别名
    router_name_set = set(router_dict.keys())

    add_name_set = router_name_set - permissions_name_set
    add_formset = AddFormSet(initial=[row for name, row in router_dict.items() if name in add_name_set])

    if request.method == 'POST' and post_type == 'add':
        add_formset = AddFormSet(request.POST)
        if add_formset.is_valid():
            permission_obj_list = [models.Permission(**i) for i in add_formset.cleaned_data]
            query_list = models.Permission.objects.bulk_create(permission_obj_list)
            add_formset = AddFormSet()
            for i in query_list:
                permissions_name_set.add(i.name)

    del_name_set = permissions_name_set - router_name_set
    del_formset = FormSet(queryset=models.Permission.objects.filter(name__in=del_name_set))

    update_name_set = permissions_name_set & router_name_set
    update_formset = FormSet(queryset=models.Permission.objects.filter(name__in=update_name_set))

    if request.method == 'POST' and post_type == 'update':
        update_formset = FormSet(request.POST)
        if update_formset.is_valid():
            update_formset.save()
            update_formset = FormSet(queryset=models.Permission.objects.filter(name__in=update_name_set))

    return render(
        request,
        'rbac/multi_permissions.html',
        {
            'del_formset': del_formset,
            'update_formset': update_formset,
            'add_formset': add_formset,
        }
    )


def distribute_permissions(request):
    """
    分配权限
    :param request:
    :return:
    """
    uid = request.GET.get('uid')
    rid = request.GET.get('rid')

    if request.method == 'POST' and request.POST.get('postType') == 'role':
        user = models.User.objects.filter(id=uid).first()
        if not user:
            return HttpResponse('用户不存在')
        user.roles.set(request.POST.getlist('roles'))

    if request.method == 'POST' and request.POST.get('postType') == 'permission' and rid:
        role = models.Role.objects.filter(id=rid).first()
        if not role:
            return HttpResponse('角色不存在')
        role.permissions.set(request.POST.getlist('permissions'))

    # 所有用户（展示在页面的最左端）
    user_list = models.User.objects.all()

    user_has_roles = models.User.objects.filter(id=uid).values('id', 'roles')

    user_has_roles_dict = {item['roles']: None for item in user_has_roles}

    # 所有的角色（展示在页面的中间）
    role_list = models.Role.objects.all()

    if rid:
        role_has_permissions = models.Role.objects.filter(id=rid, permissions__id__isnull=False).values('id',
                                                                                                        'permissions')
    elif uid and not rid:
        user = models.User.objects.filter(id=uid).first()
        if not user:
            return HttpResponse('用户不存在')
        role_has_permissions = user.roles.filter(permissions__id__isnull=False).values('id', 'permissions')
    else:
        role_has_permissions = []

    role_has_permissions_dict = {item['permissions']: None for item in role_has_permissions}

    all_menu_list = []

    queryset = models.Menu.objects.values('id', 'title')
    menu_dict = {}

    for item in queryset:
        item['children'] = []
        menu_dict[item['id']] = item
        all_menu_list.append(item)

    other = {'id': None, 'title': '其他', 'children': []}
    all_menu_list.append(other)
    menu_dict[None] = other

    root_permission = models.Permission.objects.filter(menu__isnull=False).values('id', 'title', 'menu_id')
    root_permission_dict = {}

    for per in root_permission:
        per['children'] = []
        nid = per['id']
        menu_id = per['menu_id']
        root_permission_dict[nid] = per
        menu_dict[menu_id]['children'].append(per)

    node_permission = models.Permission.objects.filter(menu__isnull=True).values('id', 'title', 'parent_id')

    for per in node_permission:
        pid = per['parent_id']
        if not pid:
            menu_dict[None]['children'].append(per)
            continue
        root_permission_dict[pid]['children'].append(per)

    return render(
        request,
        'rbac/distribute_permissions.html',
        {
            'user_list': user_list,
            'role_list': role_list,
            'user_has_roles_dict': user_has_roles_dict,
            'role_has_permissions_dict': role_has_permissions_dict,
            'all_menu_list': all_menu_list,
            'uid': uid,
            'rid': rid
        }
    )
