from django.shortcuts import render,HttpResponse
# from rest_framework.authentication import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from . import my_setting_authentication
# Create your views here.
class my_authentication(APIView):
    authentication_classes = [my_setting_authentication.my_authentication,my_setting_authentication.head_authentication,my_setting_authentication.exe]
    def get(self,request):
        return Response({"msg":"hello"})
"""
drf的认证流程
进入到dispatch方法中重新封装了request然后传给了 self.initial(request, *args, **kwargs)
self.initial(request, *args, **kwargs) 方法中调用了 self.perform_authentication(request) 方法
self.perform_authentication(request) 方法中调用了 内容 request.user 方法
而这request方法是封装后的request的所以这里调用会去到新reques找到user
这个user是一个 
@property(这是方法转换成属性：可以通过getter和setter方法控制属性的访问和修改。这有助于封装类的内部实现，防止外部直接访问和修改属性。)
def user(self):
    if not hasattr(self, '_user'):这里先从实例类进行找没有找到则进入到判断里面
        with wrap_attributeerrors():
            self._authenticate()会到这里来
        return self._user
def _authenticate(self):
        for authenticator in self.authenticators://这里是我们的认证类
            try:
                user_auth_tuple = authenticator.authenticate(self)//调用我们重新的authenticate方法进行赋值
            except exceptions.APIException:
                self._not_authenticated()
                raise
        if user_auth_tuple is not None:
                self._authenticator = authenticator保存我们认证器
                self.user, self.auth = user_auth_tuple把认证方法返回的内容赋值
                return

"""