from django.template.defaulttags import url
from django.urls import path

from .views import *

urlpatterns = [
    # 指定路由名为url_name，对应处理函数为当前app内views.py中的api_name
    # path('url_name', func_name),
    path('newfile', create_file),
    path('newteamfile', create_team_file),
    path('deletefile', delete_file),
    path('person_root_filelist', person_root_filelist),
    path('team_root_filelist', team_root_filelist),
    path('readfile', read_file),
    path('editfile', edit_file),
    path('closefile', close_file),
    path('getdirectorylist', get_file_list_of_dir),
    path('recyclebin', get_filelist_of_recycle_bin),
    path('completelydelete', completely_delete_file),
    path('restorefile', restore_file),
    path('readfile', read_file),
    path('changefilename', change_file_name),
    path('setcomment', set_comment_to),
    path('changecommentcharacter', change_comment_character),
    path('deletecomment', delete_comment),
    path('showcomment', show_comment_list),
    # url('^qrcode/(.+)$', generate_qrcode),
    path('debug_file_status', debug_file_status),
    path('last_10_read_file', last_10_read_file),
    path('create_share_link', create_share_link),
]
