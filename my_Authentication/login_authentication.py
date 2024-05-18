"""
@big_name:drf_wupeiqi	
@file_name:login_authentication	
@data:2024/5/18	
@developers:handsome_lxh
"""
# 认证案例你要有token才可以进行访问
from rest_framework.views import APIView
from rest_framework.response import Response
from . import my_setting_authentication
class my_login(APIView):
    authentication_classes = [my_setting_authentication.my_login_authentication,my_setting_authentication.my_login_head_authentication,my_setting_authentication.exe]
    # permission_classes = []
    def get(self,requests):
        username= requests.user
        token=requests.auth
        self.dispatch()
        return Response({"code":200,"message":"请求成功","data":{"username":username,"token":token}})