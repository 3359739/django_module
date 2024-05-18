"""
@big_name:drf_wupeiqi
@file_name:my_permission_initital
@data:2024/5/18
@developers:handsome_lxh
"""
from rest_framework.permissions import BasePermission

class MyPermission(BasePermission):
    message = {
        'erro': '没有权限',
        "cole": 403
    }
    def has_permission(self, request, view):
        data = request.META.get("HTTP_TOKE")
        if data == "1":
            return True
        else:
            return False  # 直接返回 False，DRF 会自动使用定义的 message 属性
class MyPermission1(BasePermission):
    message = {
        'erro': '没有权限',
        "cole": 403
    }
    def has_permission(self, request, view):
        data = request.META.get("HTTP_TOKE")
        if data == "2":
            return True
        else:
            return False  # 直接返回 False，DRF 会自动使用定义的 message 属性
