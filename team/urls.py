from django.urls import path
from .views import *

urlpatterns = [
    # 指定路由名为url_name，对应处理函数为当前app内views.py中的api_name
    path('create_team', create_team),
    path('my_team_list', my_team_list),
    path('apply_for_joining_team', apply_for_joining_team),
    path('team_info', team_info),
    path('invite', invite),
    path('debug_all_team', debug_all_team),
    path('debug_clear_team', debug_clear_team),
]