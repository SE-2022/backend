from django.urls import path
from .views import *

urlpatterns = [
    path('createtag', create_tag),
    path('addfav', add_tag_to_file)
]
