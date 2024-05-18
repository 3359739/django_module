"""
@big_name:drf_wupeiqi	
@file_name:my_setting_authentication	
@data:2024/5/17	
@developers:handsome_lxh
"""

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
class my_authentication(BaseAuthentication):
    def authenticate(self,request):
        token=request.query_params.get("token")
        # print(dir(request))
        # print(token)
        # print(request.__dir__())
        if token:
             return "用户","token"
        else:
            return
class head_authentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_TOKEN')
        print(token)
        if token:
            return "用户", "token"
        else:
            return
class exe(BaseAuthentication):
    def authenticate(self, request):
        raise AuthenticationFailed("认证失败")
from . import models
import uuid
# 从参数获取
class my_login_authentication(BaseAuthentication):
    def authenticate(self, request):
        username = request.query_params.get("username")
        password = request.query_params.get("password")
        substance=models.user_login.objects.filter(username=username,password=password).first()
        if substance:
            print("我是请求参数认证成功的")
            token=uuid.uuid4()
            substance.token=token
            substance.save()
            return substance,token

        else:
           return


class my_login_head_authentication(BaseAuthentication):
    def authenticate(self, request):
        token=request.META.get('HTTP_TOKEN')
        substance = models.user_login.objects.filter(token=token).first()
        if substance:
            print("我是请求头认证成功的")
            return substance.username, token
        else:
            return
