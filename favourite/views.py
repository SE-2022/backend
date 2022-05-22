from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from favourite.models import Tag, TagFile
from file.models import File
from user.models import User
from utility.utility import login_check


@csrf_exempt
def create_tag(request):
    if not request.method == 'POST':
        return JsonResponse({'errno': 3010, 'msg': "请求方式错误"})
    if not login_check(request):
        return JsonResponse({'errno': 3009, 'msg': "用户未登录"})
    try:
        tag_name = request.method.get('tag_name')
    except ValueError:
        return JsonResponse({'errno': 3001, 'msg': "标签名不得为空"})
    except Exception as e:
        return JsonResponse({'errno': 3000, 'msg': repr(e)})
    user = User.objects.get(userID=request.session['userID'])
    tag_cur = Tag.objects.filter(tag_name=tag_name)
    if tag_cur.count() > 0:
        return JsonResponse({'errno': 3002, 'msg': "标签已存在"})
    tag = Tag(tag_name=tag_name, user=user)
    tag.save()
    return JsonResponse({'errno': 0, 'msg': "新建标签成功", 'tagID': tag.tagID})


@csrf_exempt
def add_tag_to_file(request):
    if not request.method == 'POST':
        return JsonResponse({'errno': 3010, 'msg': "请求方式错误"})
    if not login_check(request):
        return JsonResponse({'errno': 3009, 'msg': "用户未登录"})
    try:
        fileid = request.method.get('fileid')
        tag_id = request.method.get('tag_id')
    except ValueError:
        return JsonResponse({'errno': 3003, 'msg': "信息获取失败"})
    user = User.objects.get(userID=request.session['userID'])
    relation_tmp = TagFile.objects.filter(file=File.objects.get(fileid=fileid), tag=Tag.objects.get(tagID=tag_id),
                                          user=user)
    if relation_tmp.count() >= 1:
        return JsonResponse({'errno': 3004, 'msg': "文件已在此标签下"})
    rel = TagFile(file=File.objects.get(fileid=fileid), tag=Tag.objects.get(tagID=tag_id), user=user)
    rel.save()
    return JsonResponse({'errno': 0, 'msg': "收藏成功"})


@csrf_exempt
def get_tag_msg(request):
    if not request.method == 'POST':
        return JsonResponse({'errno': 3010, 'msg': "请求方式错误"})
    if not login_check(request):
        return JsonResponse({'errno': 3009, 'msg': "用户未登录"})
    try:
        tag_id = request.method.get('tag_id')
    except ValueError:
        return JsonResponse({'errno': 3003, 'msg': "信息获取失败"})
    user = User.objects.get(userID=request.session['userID'])
    tag = Tag.objects.get(tagID=tag_id, user=user)
    res_list = []
    tag_list = TagFile.objects.filter(user=user, tag=tag)
    for i in tag_list:
        res_list.append({"filename": i.file.file_name, "create_time": i.file.create_time, "tag_file_relationID": i.id,
                         "author": user.username})
    return JsonResponse({'errno': 0, 'msg': "筛选成功", 'tag_file_list': res_list})


@csrf_exempt
def remove_tag(request):
    if request.method == 'POST':
        if login_check(request):
            try:
                tag_id = request.method.get('tag_id')
            except ValueError:
                return JsonResponse({'errno': 3003, 'msg': "标签信息获取失败"})
            user = User.objects.get(userID=request.session['userID'])
            tag = Tag.objects.get(user=user, tagID=tag_id)
            tag.delete()
            return JsonResponse({'errno': 0, 'msg': "删除成功"})
        else:
            return JsonResponse({'errno': 3009, 'msg': "用户未登录"})
    else:
        return JsonResponse({'errno': 3010, 'msg': "请求方式错误"})


def rename_tag(request):
    if not request.method == 'POST':
        return JsonResponse({'errno': 3010, 'msg': "请求方式错误"})
    if not login_check(request):
        return JsonResponse({'errno': 3009, 'msg': "用户未登录"})
    try:
        tag_id = request.method.get('tag_id')
        new_tag_name = request.method.get('new_tag_name')
    except ValueError:
        return JsonResponse({'errno': 3003, 'msg': "信息获取失败"})
    user = User.objects.get(userID=request.session['userID'])
    try:
        tag = Tag.objects.get(tagID=tag_id, user=user)
        if tag.DoesNotExist:
            raise ValueError("无法获取标签信息")
    except ValueError as e:
        return JsonResponse({'errno': 3005, 'msg': repr(e)})
    tag.tag_name = new_tag_name
    tag.save()
    return JsonResponse({'errno': 0, 'msg': "修改成功", 'tagID': tag.tagID})
