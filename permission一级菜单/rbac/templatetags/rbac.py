# __author: busensei
# data: 2018/10/30
import re
from django import template
from django.conf import settings

register = template.Library()


@register.inclusion_tag('rbac/menu.html')
def menu(request):
    menu_list = request.session.get(settings.MENU_SESSION_KEY)
    for item in menu_list:
        url = item.get('url')
        if re.match('^{}$'.format(url), request.path_info):
            item['class'] = 'active'
    return {"menu_list": menu_list}
