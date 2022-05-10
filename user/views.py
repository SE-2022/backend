from django.db import IntegrityError
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.contrib.auth.hashers import make_password, check_password
import smtplib
from django.core.exceptions import *

# from django.contrib.auth.models import User
from user.models import User
# Create your views here.
from django.views.decorators.csrf import csrf_exempt


def send_email(target, content):
    return


def password_check(password):
    return len(password) >= 8


def res(number, message):
    return JsonResponse({'errno': number, "msg": message})


def login_check(request):
    return 'userID' in request.session


def userinfo_check(user):
    return user.username is not None and user.password is not None and user.email is not None


def username_exist(username):
    user_list = User.objects.filter(username=username)
    return len(list(user_list)) != 0

@csrf_exempt
def register(request):
    if request.method == 'POST':
        # 获取信息
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')
        except ValueError:
            return JsonResponse({'errno': 1002, 'msg': '缺少字段'})
        except Exception as e:
            return JsonResponse({'errno': 1001, 'msg':repr(e)})
        # 用户名不得重复
        if username_exist(username):
            return res(1009, "用户名已被注册")
        # 生成user对象
            return JsonResponse({'errno': 1001, 'msg': repr(e)})



@csrf_exempt
def login(request):
    if request.method == 'POST':
        # 获取信息
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
        except ValueError:
            return JsonResponse({'errno': 1002, 'msg': '缺少字段'})
        except Exception as e:
            return JsonResponse({'errno': 1001, 'msg': repr(e)})
        # 检查
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return res(1004,'用户名不存在')
        except MultipleObjectsReturned:
            return res(1001,'数据库中存在多个相同的用户名，这是一个bug')
        if not check_password(password, user.password):
            return res(1005,'密码错误')
        # 通过检查
        request.session['userID'] = user.userID
        return res(1000, '登陆成功')
    else:
        return res(1, '请求方式错误')


@csrf_exempt
def logout(request):
    if request.method == 'POST':
        request.session.flush()
        return res(1000, '注销成功')
    else:
        return res(1, '请求方式错误')


@csrf_exempt
def get_user_info(request):
    if request.method != 'POST':
        return res(1, '请求方式错误')
    if not login_check(request):
        return res(1006, '用户未登录')
    user = User.objects.get(userID=request.session['userID'])
    return JsonResponse({'errno': 1000, 'msg': '获取个人信息成功',
                         'user_info': {
                             'userID': user.userID,
                             'username': user.username,
                             'email': user.email,
                         }})


@csrf_exempt
def edit_user_info(request):
    if request.method != 'POST':
        return res(1, '请求方式错误')
    if not login_check(request):
        return res(1006,'用户未登录')
    # 获取信息
    user = User.objects.get(userID=request.session['userID'])
    user.username = request.POST.get('username')
    user.password = request.POST.get('password')
    user.email = request.POST.get('email')
    # 各字段不能为空
    if not userinfo_check(user) or not password_check(user.password):
        return res(1007,'个人信息填写有误')
    # 用户名不得与现有的重复
    if username_exist(user.username):
        return res(1010, "用户名已被注册")
    user.password = make_password(user.password)
    user.save()
    return res(1000, '编辑个人信息成功')


@csrf_exempt
def get_user_avatar(request):
    if request.method != 'POST':
        return res(1, '请求方式错误')
    if not login_check(request):
        return res(1006, '用户未登录')
    user = User.objects.get(userID=request.session['userID'])
    return HttpResponse(user.avatar.read(), content_type='image')


@csrf_exempt
def edit_user_avatar(request):
    if request.method != 'POST':
        return res(1, '请求方式错误')
    if not login_check(request):
        return res(1006, '用户未登录')
    if 'avatar' not in request.FILES:
        return res(1008, '个人头像上传失败')
    user = User.objects.get(userID=request.session['userID'])
    user.avatar = request.FILES.get('avatar')
    if user.avatar is None:
        return res(1008, '个人头像上传失败')
    user.save()
    return res(1000, '编辑个人头像成功')
