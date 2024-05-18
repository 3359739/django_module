"""
@big_name:drf_wupeiqi	
@file_name:urls	
@data:2024/5/17	
@developers:handsome_lxh
"""

from django.urls import path
from . import views
from . import login_authentication
urlpatterns = [
    path("my_authentication_initital/",views.my_authentication.as_view()),
    path("my_authentication_login/",login_authentication.my_login.as_view())
]