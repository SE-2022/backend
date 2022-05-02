# from django.contrib.postgres import serializers
import json

from django.core import serializers
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from Diamond.models import User, File


@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        user = User.objects.filter(username=username)
        if user.count() != 0:
            return JsonResponse({'errno': 1014, 'msg': "用户名已存在"})
        if password1 != password2:
            return JsonResponse({'errno': 1013, 'msg': "两次输入的密码不一致"})
        else:
            new_user = User(username=username, password=password1)
            new_user.save()
            return JsonResponse({'errno': 0, 'msg': "注册成功"})
    else:
        return JsonResponse({'errno': 1012, 'msg': "请求方式错误"})


def filelist(username):
    l = File.objects.filter(username=username)
    res = []
    for i in l:
        res.append({"fileName": i.file_name, "createTime": i.create_time, "lastEditTime": i.last_modify_time})
    return res


@csrf_exempt
def create_file(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        file_name = request.POST.get('file_name')
        user = User.objects.filter(username=username)
        file = File.objects.filter(file_name=file_name)
        if user.count() == 0:  # 用户名不存在
            return JsonResponse({'errno': 1015, 'msg': "文件创建失败"})
        elif file.count() != 0:
            return JsonResponse({'errno': 1015, 'msg': "文件创建失败"})
        else:
            # new_file = File(username=username, file_name=file_name)
            new_file = File()
            new_file.file_name = file_name
            new_file.username = username
            new_file.save()
            # print(username, file_name, new_file.create_time, new_file.last_modify_time)
            result = {'errno': 0, 'msg': "文件创建成功", 'fileList': filelist(username)}
            # file_list = File.objects.filter(username=username)
            # for var in file_list:
            #     result['fileList'].append(
            #         {"fileName": var.file_name, "createTime": var.create_time, "lastEditTime": var.last_modify_time})
            return JsonResponse(result)
    else:
        return JsonResponse({'errno': 1012, 'msg': "请求方式错误"})


@csrf_exempt
def get_filelist(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = User.objects.filter(username=username)
        if user.count() == 0:
            return JsonResponse({'errno': 1011, 'msg': "用户不存在"})
        else:
            return JsonResponse({'fileList': filelist(username)})
    else:
        return JsonResponse({'errno': 1012, 'msg': "请求方式错误"})


@csrf_exempt
def delete_file(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        filename = request.POST.get('fileName')
        user = User.objects.filter(username=username)
        if user.count() == 0:
            return JsonResponse({'errno': 1011, 'msg': "用户不存在"})
        file = File.objects.filter(username=username, file_name=filename)
        if file.count() == 0:
            return JsonResponse({'errno': 1016, 'msg': "此文件不存在", 'fileList': filelist(username)})
        file.delete()
        return JsonResponse({'errno': 0, 'msg': "删除成功", 'fileList': filelist(username)})