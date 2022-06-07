from django.urls import path
from .views import *

urlpatterns = [
    path('createtag', create_tag),
    path('addfav', add_tag_to_file),
    path('getTagMsg', get_tag_msg),
    path('removeTag', remove_tag),
    path('renameTag', rename_tag),
    path('showTags', show_tags),
    path('removeTagFile', remove_tag_file),
    path('changeColor', change_color),
    path('changeDetails', change_details),
    path('showfav', show_all_fav_file)
]
