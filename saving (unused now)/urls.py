# publish (unused now)/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('save', save),
    path('load', load),
    path('getFileList', getFileList ),
    path('delete', delete),
    path('create', create),
    # 这是一个样例，指定路由名为url_name，对应处理函数为当前app内views.py中的api_name
]