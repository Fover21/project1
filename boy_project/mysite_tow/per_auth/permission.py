# __author: ward
# data: 2018/11/17
from rest_framework.permissions import BasePermission


# class MyPermission(object):
#     message = '权限不足'
#
#     def has_permission(self, request, view):
#         # 权限逻辑
#         # 认证已经执行完了
#         user_obj = request.user
#         print(user_obj)
#         try:
#             if user_obj.type == 1:
#                 return False
#             else:
#                 return True
#         except Exception as e:
#             print(e)
#             return False


class MyPermission(BasePermission):
    message = '权限不足'

    def has_permission(self, request, view):
        # 权限逻辑
        # 认证已经执行完了
        user_obj = request.user
        print(user_obj)
        try:
            if user_obj.type == 1:
                return False
            else:
                return True
        except Exception as e:
            print(e)
            return False