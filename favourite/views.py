from django.core.exceptions import ObjectDoesNotExist
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
        tag_name = request.POST.get('tag_name')
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
        fileid = request.POST.get('fileid')
        tag_id = request.POST.get('tag_id')
    except ValueError:
        return JsonResponse({'errno': 3003, 'msg': "信息获取失败"})
    user = User.objects.get(userID=request.session['userID'])
    try:
        file = File.objects.get(fileID=fileid, isDelete=False, isDir=False)
    except ObjectDoesNotExist:
        return JsonResponse({'errno': 3003, 'msg': "信息获取失败"})
    relation_tmp = TagFile.objects.filter(file=file, tag=Tag.objects.get(tagID=tag_id),
                                          user=user)
    if relation_tmp.count() >= 1:
        return JsonResponse({'errno': 3004, 'msg': "文件已在此标签下"})
    rel = TagFile(file=file, tag=Tag.objects.get(tagID=tag_id), user=user)
    rel.save()
    return JsonResponse({'errno': 0, 'msg': "收藏成功"})


@csrf_exempt
def get_tag_msg(request):
    if not request.method == 'POST':
        return JsonResponse({'errno': 3010, 'msg': "请求方式错误"})
    if not login_check(request):
        return JsonResponse({'errno': 3009, 'msg': "用户未登录"})
    try:
        tag_id = request.POST.get('tag_id')
    except ValueError:
        return JsonResponse({'errno': 3003, 'msg': "信息获取失败"})
    user = User.objects.get(userID=request.session['userID'])
    try:
        tag = Tag.objects.get(tagID=tag_id, user=user)
    except ObjectDoesNotExist:
        return JsonResponse({'errno': 3003, 'msg': "信息获取失败"})
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
                tag_id = request.POST.get('tag_id')
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


@csrf_exempt
def rename_tag(request):
    if not request.method == 'POST':
        return JsonResponse({'errno': 3010, 'msg': "请求方式错误"})
    if not login_check(request):
        return JsonResponse({'errno': 3009, 'msg': "用户未登录"})
    try:
        tag_id = request.POST.get('tag_id')
        new_tag_name = request.POST.get('new_tag_name')
    except ValueError:
        return JsonResponse({'errno': 3003, 'msg': "信息获取失败"})
    user = User.objects.get(userID=request.session['userID'])
    try:
        tag = Tag.objects.get(tagID=tag_id, user=user)
        # if tag.DoesNotExist:
        #     raise ValueError("无法获取标签信息")
    except ObjectDoesNotExist:
        return JsonResponse({'errno': 3005, 'msg': "无法获取标签信息"})
    tag.tag_name = new_tag_name
    tag.save()
    return JsonResponse({'errno': 0, 'msg': "修改成功", 'tagID': tag.tagID, 'tag_name': tag.tag_name})


@csrf_exempt
def show_tags(request):
    if not request.method == 'POST':
        return JsonResponse({'errno': 3010, 'msg': "请求方式错误"})
    if not login_check(request):
        return JsonResponse({'errno': 3009, 'msg': "用户未登录"})
    user = User.objects.get(userID=request.session['userID'])
    try:
        tag_list = Tag.objects.filter(user=user)
    except ObjectDoesNotExist:
        return JsonResponse({'errno': 3006, 'msg': "标签集为空"})
    res = []
    for i in tag_list:
        res.append({'tagID': i.tagID, 'tag_name': i.tag_name})
    return JsonResponse({'errno': 0, 'tag_list': res})


@csrf_exempt
def remove_tag_file(request):
    if not request.method == 'POST':
        return JsonResponse({'errno': 3010, 'msg': "请求方式错误"})
    if not login_check(request):
        return JsonResponse({'errno': 3009, 'msg': "用户未登录"})
    try:
        tag_id = request.POST.get('tag_id')
        fileid = request.POST.get('fileid')
    except ValueError:
        return JsonResponse({'errno': 3003, 'msg': "信息获取失败"})

    try:
        file = File.objects.get(fileID=fileid)
    except ObjectDoesNotExist:
        return JsonResponse({'errno': 3007, 'msg': "文件信息获取失败"})
    try:
        tag = Tag.objects.get(tagID=tag_id)
    except ObjectDoesNotExist:
        return JsonResponse({'errno': 3008, 'msg': "标签信息获取失败"})
    user = User.objects.get(userID=request.session['userID'])
    try:
        file_tag_relation = TagFile.objects.get(file=file, tag=tag, user=user)
    except ObjectDoesNotExist:
        return JsonResponse({'errno': 3011, 'msg': "文件不在此标签下"})
    file_tag_relation.delete()
    return JsonResponse({'errno': 0, 'msg': "取消收藏成功"})
