"""
@Author：WangYuXiang
@E-mile：Hill@3io.cc
@CreateTime：2021/4/25 16:51
@DependencyLibrary：无
@MainFunction：无
@FileDoc： 
    permissions.py
    文件说明
@ChangeHistory:
    datetime action why
    example:
    2021/4/25 16:51 change 'Fix bug'
        
"""
from sanic_rest_framework.exceptions import APIException
from sanic_rest_framework.status import HttpStatus


class BaseCheckPermission:
    async def has_permission(self, request, view):
        pass

    async def has_obj_permission(self, request, view, obj):
        pass


class CheckPermissionByAnyCode(BaseCheckPermission):
    def __init__(self, codes: iter):
        self.codes = codes

    async def has_permission(self, request, view):
        if not request.user.has_permissions(self.codes):
            raise APIException(message='无权限进行此操作', http_status=HttpStatus.HTTP_403_FORBIDDEN)

    async def has_obj_permission(self, request, view, obj):
        pass
