# __author: busensei
# data: 2018/10/30
import re
from collections import OrderedDict
from django import template
from django.conf import settings

register = template.Library()


# @register.inclusion_tag('rbac/menu.html')
# def menu(request):
#     menu_list = request.session.get(settings.MENU_SESSION_KEY)
#     for item in menu_list.values():
#         for i in item['children']:
#             if re.match('^{}$'.format(i['url']), request.path_info):
#                 i['class'] = 'active'
#     return {"menu_list": menu_list}

# @register.inclusion_tag('rbac/menu.html')
# def menu(request):
#     menu_list = request.session.get(settings.MENU_SESSION_KEY)
#     order_dict = OrderedDict()
#     for i in sorted(menu_list, reverse=True):
#         order_dict[i] = menu_list[i]
#
#     for item in order_dict.values():
#         for i in item['children']:
#             if re.match('^{}$'.format(i['url']), request.path_info):
#                 i['class'] = 'active'
#     return {"menu_list": order_dict}

# @register.inclusion_tag('rbac/menu.html')
# def menu(request):
#     menu_list = request.session.get(settings.MENU_SESSION_KEY)
#     order_dict = OrderedDict()
#     for i in sorted(menu_list, key=lambda x: menu_list[x]['weight'], reverse=True):
#         order_dict[i] = menu_list[i]
#
#     for item in order_dict.values():
#         item['class'] = 'hide'
#
#         for i in item['children']:
#             if re.match('^{}$'.format(i['url']), request.path_info):
#                 i['class'] = 'active'
#                 item['class'] = ''
#     return {"menu_list": order_dict}

# @register.inclusion_tag('rbac/menu.html')
# def menu(request):
#     menu_list = request.session.get(settings.MENU_SESSION_KEY)
#     order_dict = OrderedDict()
#
#     for key in sorted(menu_list, key=lambda x: menu_list[x]['weight'], reverse=True):
#         item = order_dict[key] = menu_list[key]
#         item['class'] = 'hide'
#
#         for i in item['children']:
#             if re.match('^{}$'.format(i['url']), request.path_info):
#                 i['class'] = 'active'
#                 item['class'] = ''
#     return {"menu_list": order_dict}

@register.inclusion_tag('rbac/menu.html')
def menu(request):
    menu_list = request.session.get(settings.MENU_SESSION_KEY)
    order_dict = OrderedDict()

    for key in sorted(menu_list, key=lambda x: menu_list[x]['weight'], reverse=True):
        order_dict[key] = menu_list[key]
        item = order_dict[key]
        item['class'] = 'hide'

        for i in item['children']:

            if i['id'] == request.current_menu_id:
                i['class'] = 'active'
                item['class'] = ''
    return {"menu_list": order_dict}


@register.inclusion_tag('rbac/ssssss.html')
def breadcrumb(request):
    return {"breadcrumd_list": request.breadcrumd_list}


@register.filter
def has_permission(request, permission):
    if permission in request.session.get(settings.PERMISSION_SESSION_KEY):
        return True
