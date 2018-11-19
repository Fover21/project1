# __author: busensei
# data: 2018/11/19

from rest_framework import pagination


class MyPaginator(pagination.PageNumberPagination):
    # 每页限制数量
    page_size = 2
    # 参数
    page_query_param = 'page_num'
    page_size_query_param = 'size'
    # 限制
    max_page_size = 3


class MyLimitOffset(pagination.LimitOffsetPagination):
    default_limit = 1
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = 999


class MyCursorPagination(pagination.CursorPagination):
    cursor_query_param = 'cursor'
    page_size = 1
    ordering = '-id'