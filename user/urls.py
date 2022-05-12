from django.urls import path
from .views import *

urlpatterns = [
    # 指定路由名为url_name，对应处理函数为当前app内views.py中的api_name
    path('register', register),
    path('login', login),
    path('logout', logout),
    path('get_user_info', get_user_info),
    path('edit_user_info', edit_user_info),
    path('get_user_avatar', get_user_avatar),
    path('edit_user_avatar', edit_user_avatar),
    path('debug_get_user_list', debug_get_user_list),
    path('debug_clear_user', debug_clear_user),
    path('debug_status', debug_status),
]
