"""
@big_name:drf_wupeiqi	
@file_name:urls	
@data:2024/5/18	
@developers:handsome_lxh
"""
from django.urls import path
from . import views
urlpatterns=[
    path("my_throttle/",views.MyThrottle.as_view())
]