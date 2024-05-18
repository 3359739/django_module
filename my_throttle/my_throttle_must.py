"""
@big_name:drf_wupeiqi	
@file_name:my_throttle_must	
@data:2024/5/18	
@developers:handsome_lxh
"""
from rest_framework.throttling import SimpleRateThrottle
from django.core.cache import cache
from rest_framework import exceptions
from rest_framework import status

class ThrottledException(exceptions.APIException):
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    default_code = 'throttled'
class MyThrottleMust(SimpleRateThrottle):
    scope = 'lxh'
    cache = cache
    cache_format = 'throttle_%(scope)s_%(ident)s'
    THROTTLE_RATES = {"lxh": "10/m"}
    def get_cache_key(self, request, view):
        if request.user:
            ident = request.user.pk  # 用户ID
            print(request.user)
        else:
            ident = self.get_ident(request)  # 获取请求用户IP（去request中找请求头）
        return self.cache_format % {'scope': self.scope, 'ident': ident}

    def throttle_failure(self):
        wait = self.wait()
        detail = {
            "code": 1005,
            "data": "访问频率限制",
            'detail': "需等待{}s才能访问".format(int(wait))
        }
        raise ThrottledException(detail)