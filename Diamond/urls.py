
from django.urls import path
from .views import *

urlpatterns = [
    path('register', register),
    path('createFile', create_file),
    path('getFileList', get_filelist),
    path('deleteFile', delete_file)
]
