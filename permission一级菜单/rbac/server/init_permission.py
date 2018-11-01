# __author: ward
# data: 2018/10/30
from django.conf import settings


def init_permission(request, user):
    # 1. 查当前登录用户拥有的权限
    permission_query = user.roles.filter(permissions__url__isnull=False).values(
        'permissions__url',
        'permissions__is_menu',
        'permissions__icon',
        'permissions__title'
    ).distinct()
    print('permission_query', permission_query)
    # 存放权限信息
    permission_list = []
    # 存放菜单信息
    menu_list = []
    for item in permission_query:
        permission_list.append({'url': item['permissions__url']})
        if item.get('permissions__is_menu'):
            menu_list.append({
                'url': item['permissions__url'],
                'icon': item['permissions__icon'],
                'title': item['permissions__title'],
            })

    # 2. 将权限信息写入到session
    request.session[settings.PERMISSION_SESSION_KEY] = permission_list
    # 将菜单的信息写入到session中
    request.session[settings.MENU_SESSION_KEY] = menu_list
    print('request.session', request.session)
    print('request.session', request.session.get('permissions'))
    print('request.session', request.session.get('menus'))
