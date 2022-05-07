from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.hashers import make_password, check_password
import smtplib

# from django.contrib.auth.models import User
from user.models import User
# Create your views here.
from django.views.decorators.csrf import csrf_exempt


def send_email(target, content):
    return


def password_check(password):
    return len(password) >= 8;


def res(number, message):
    return JsonResponse({'errno':number,"msg":message})


def login_check(request):
    return 'userID' in request.session


def userinfo_check(user):
    return username is not None and password is not None and email is not None


@csrf_exempt
def register(request):
    if request.method == 'POST':
        # 获取信息
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')
        except ValueError:
            return JsonResponse({'errno': 1002, 'msg':'缺少字段'})
        except Exception as e:
            return JsonResponse({'errno': 1001, 'msg':repr(e)})
        user = User(username=username,
                    password=make_password(password),
                    email=email)
        # 检查
        if not userinfo_check(user):
            return JsonResponse({'errno': 1002, 'msg': '缺少字段'})
        if not password_check(password):
            return JsonResponse({'errno': 1003, 'msg': '密码太弱'})
        # 保存
        try:
            user.save()
        except Exception as e:
            return JsonResponse({'errno': 1001, 'msg': repr(e)})
        # except
        return JsonResponse({'errno': 1000, 'msg': '注册成功'})
    else:
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


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
        except Exception:
            return res(1004,'用户名不存在')
        if not check_password(password, user.password):
            return res(1005,'密码错误')
        request.session['userID'] = user.userID
        return res(1000,'登陆成功')
    else:
        return res(1,'请求方式错误')


@csrf_exempt
def logout(request):
    if request.method == 'POST':
        request.session.flush()
        return res(1000,'注销成功')
    else:
        return res(1,'请求方式错误')


def edit_user_info(request):
    # username
    # password
    # email
    if request.method != 'POST':
        return res(1,'请求方式错误')
    if not login_check(request):
        return res(1006,'用户未登录')
    user = User.objects.get(userID=request.session['userID'])
    # 获取信息
    user.username = request.POST.get('username')
    user.password = request.POST.get('password')
    user.email = request.POST.get('email')
    if not userinfo_check(user) or not password_check(user.password):
        return res(1007,'个人信息填写有误')
    user.save()
    return res(1000,'编辑个人信息成功')


def edit_user_avatar(request):
    if request.method != 'POST':
        return res(1,'请求方式错误')
    if not login_check(request):
        return res(1006,'用户未登录')
    user = User.objects.get(userID=request.session['userID'])
    user.avatar = request.POST.get('avatar')
    if user.avatar is None:
        return res(1008,'个人头像上传失败')
    user.save
    return res(1000,'编辑个人头像成功')