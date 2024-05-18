from django.shortcuts import render,HttpResponse
from rest_framework.views import APIView
# Create your views here.
from rest_framework.response import Response
from .my_permission_initital import *
class MyView(APIView):
    # authentication_classes = []
    permission_classes = [MyPermission,MyPermission1]
    def get(self, request):
        self.dispatch()
        return Response("Hello, world!")


    def check_permissions(self, request):
           substance=False
           for permission in self.get_permissions():#获得所有类进行遍历
                if permission.has_permission(request, self):#然后进行调用
                    self.substance=True#要是有一个类返回True则 substance为True表有权限登录
                    return
           if not substance:
                self.permission_denied(request,message=getattr(permission, 'message', None),code=getattr(permission, 'code', None))


"""
权限类from rest_framework.permissions import BasePermission
先进入到self.dispatch()然后进行self.initial(request, *args, **kwargs)
self.perform_authentication(request)进行认证之后会走到
self.check_permissions(request)进入到权限认证
check_permissions分析：
   1.遍历权限类，进行权限认证：self.get_permissions()先去本类中找权限类，如果没有再到父类中找在类中定义permission_classes=[]方法会覆盖调setting里面的配置
   def check_permissions(self, request):
        for permission in self.get_permissions():这里拿自定义取权限类然后进行遍历
            if not permission.has_permission(request, self):
            调用类里面的has_permission方法要是为false就会不在进行遍历调用permission_denied方法进行返回不满足权限
             这里会遍历执行自定义的权限类，要是有一个权限类不满足权限就会跳出循环
                self.permission_denied(
                    request,
                    message=getattr(permission, 'message', None),
                    code=getattr(permission, 'code', None)
                )
执行先后dispatch-》initial-》perform_authentication-》check_permissions
"""