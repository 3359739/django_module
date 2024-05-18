from django.shortcuts import render
from rest_framework.views import APIView
# Create your views here.
from .my_throttle_must import MyThrottleMust
from rest_framework.response import Response
from my_Authentication.my_setting_authentication import my_login_authentication
class MyThrottle(APIView):
    authentication_classes = [my_login_authentication]
    throttle_classes = [MyThrottleMust]
    def get(self,req):
        # self.dispatch()
        return Response({"code":"200"})
