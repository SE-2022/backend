from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import *
from django.http import HttpResponse
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from file.models import File
# from django.contrib.auth.models import User
from user.models import User
from utility.utility import *

from datetime import datetime

from team.models import Team_User


def send_email(target, content):
    return


def password_check(password):
    return len(password) >= 8


def userinfo_check(user):
    return user.username is not None and user.password is not None and user.email is not None


def username_exist(username):
    user_list = User.objects.filter(username=username)
    return len(list(user_list)) != 0


def email_exist(email):
    email_list = User.objects.filter(email=email)
    return len(email_list) != 0


login_dic = {}


@csrf_exempt
def register(request):
    if request.method == 'POST':
        # 获取信息
        vals = post_getAll(request, 'username', 'password', 'email')
        lack, lack_list = check_lack(vals)
        if lack:
            return lack_err(lack_list)
        # 用户名不得重复
        if username_exist(vals['username']):
            return res(1009, '用户名 '+vals['username']+' 已被注册')
        # 邮箱不得重复
        if email_exist(vals['email']):
            return res(1013, '邮箱 '+vals['email']+' 已被注册')
        # 密码强度检查
        if not password_check(vals['password']):
            return JsonResponse({'errno': 1003, 'msg': '密码太弱'})
        # 生成user对象
        user = User(
            username=vals['username'],
            password=make_password(vals['password']),
            email=vals['email'],
        )
        # 尝试保存user
        try:
            user.save()
        except Exception as e:
            return JsonResponse({'errno': 1001, 'msg': repr(e)})
        # 创建根文件夹
        file = File(
            fatherID=-1,
            isDir=True,
            file_name='root',
            username=user.username,
            user=user,
            commentFul=False,
            isDelete=False
        )
        try:
            file.save()
        except Exception:
            user.delete()
            return res(1012, "用户根文件夹创建失败")
        user.root_file = file
        user.save()
        # except
        return JsonResponse({'errno': 0, 'msg': '注册成功'})
    else:
        return JsonResponse({'errno': 2, 'msg': "请求方式错误"})


@csrf_exempt
def login(request):
    if request.method == 'POST':
        # if login_check(request):
        #     return res(1011, '当前客户端已经处于登录状态，这种情况下前端不应该给用户再次登录的机会，我想这是一个前端的bug')
        # print(request.session['userID'])
        # 获取信息
        vals = post_getAll(request, 'username', 'password')
        lack, lack_list = check_lack(vals)
        if lack:
            return lack_err(lack_list)
        try:
            user = User.objects.get(username=vals['username'])
        except ObjectDoesNotExist:
            return res(1004, '用户名不存在')
        except MultipleObjectsReturned:
            return res(1001, '数据库中存在多个相同的用户名，这是一个bug')
        if not check_password(vals['password'], user.password):
            return res(1005, '密码错误')
        # 通过检查
        request.session['userID'] = user.userID
        login_dic[user.username] = request.session
        return res(0, '登陆成功')
    else:
        return res(2, '请求方式错误')


@csrf_exempt
def logout(request):
    if request.method == 'POST':
        if not login_check(request):
            return res(3, '未登录不能登出')
        userID = request.session['userID']
        user = User.objects.get(userID=userID)
        request.session.flush()
        login_dic.pop(user.username)
        return res(0, '注销成功')
    else:
        return res(2, '请求方式错误')


@csrf_exempt
def get_user_info(request):
    if request.method != 'POST':
        return res(1, '请求方式错误')
    if not login_check(request):
        return need_login()
    user = User.objects.get(userID=request.session['userID'])
    team_cnt = len(Team_User.objects.filter(user=user))
    file_cnt = len(File.objects.filter(user=user))
    diff = timezone.now() - user.register_time
    dates = diff.days
    seconds = diff.seconds

    return JsonResponse({'errno': 0, 'msg': '获取个人信息成功',
                         'user_info': {
                             'userID': user.userID,
                             'username': user.username,
                             'email': user.email,
                             'phone': user.phone,
                             'information': user.information,
                             'team_count': team_cnt,
                             'file_count': file_cnt,
                             'date_count': dates,
                             'seconds_count': seconds,
                             'avatar_url': 'http://123.57.69.30/api/user/get_user_avatar',
                         }})


@csrf_exempt
def edit_user_info(request):
    if request.method != 'POST':
        return res(1, '请求方式错误')
    if not login_check(request):
        return need_login()
    # 获取信息
    vals = post_getAll(request, 'username',
                       'email', 'phone', 'information')
    lack, lack_list = check_lack(vals)
    message = ""
    user = User.objects.get(userID=request.session['userID'])
    # 尝试修改用户名
    if vals['username']!=user.username and username_exist(vals['username']):
        message += "用户名"+user.username+"已被注册\n"
    user.username = vals['username']
    # 修改email、phone、information，不进行检查
    user.email = vals['email']
    user.phone = vals['phone']
    user.information = vals['information']
    # 完成所有修改，保存
    message += "其余修改成功\n"
    user.save()
    return JsonResponse({
        'errno': 0,
        'msg': message,
    })

@csrf_exempt
def edit_password(request):
    if request.method != 'POST':
        return res(1, '请求方式错误')
    if not login_check(request):
        return need_login()
    vals = post_getAll(request, "old_password", "new_password")
    lack, lack_list = check_lack(vals)
    if lack:
        return lack_err(lack_list)
    user = User.objects.get(userID=request.session['userID'])
    if check_password(vals['old_password'], user.password):
        if password_check(vals['new_password']):
            user.password = make_password(vals['new_password'])
            user.save()
            return res(0, "修改密码成功")
        else:
            return res(1005, "新密码太弱")
    return res(1003, "旧密码错误")


@csrf_exempt
def get_user_avatar(request):
    # if request.method != 'POST':
    #     return res(1, '请求方式错误')
    if not login_check(request):
        return need_login()
    user = User.objects.get(userID=request.session['userID'])
    return HttpResponse(user.avatar.read(), content_type='image/png')


@csrf_exempt
def edit_user_avatar(request):
    if request.method != 'POST':
        return res(2, '请求方式错误')
    if not login_check(request):
        return need_login()
    if 'avatar' not in request.FILES:
        return res(1008, '个人头像上传失败')
    user = User.objects.get(userID=request.session['userID'])
    user.avatar = request.FILES.get('avatar')
    if user.avatar is None:
        return res(1008, '个人头像上传失败')
    user.save()
    return res(0, '编辑个人头像成功')


@csrf_exempt
def get_status(request):
    if login_check(request):
        return JsonResponse({
            'login': True,
            'username': User.objects.get(userID=request.session['userID']).username
        })
    return JsonResponse({'login': False})


# 获取全部注册用户的列表
@csrf_exempt
def debug_get_user_list(request):
    if request.method != 'POST':
        return res(1, '请求方式错误')
    user_list = User.objects.all()
    result = []
    for user in user_list:
        result.append(user.to_dict())
    return JsonResponse(result, safe=False)


@csrf_exempt
def debug_get_login_list(request):
    login_list = []
    for key in login_dic.keys():
        login_list.append(key)
    return JsonResponse(login_list, safe=False)


# 清除所有注册用户
@csrf_exempt
def debug_clear_user(request):
    user_list = User.objects.all()
    cnt = 0
    for user in user_list:
        user.delete()
        cnt += 1
    return res(10086, '成功删除' + str(cnt) + '个用户')


@csrf_exempt
def debug_everyone_logout(request):
    for name, se in login_dic.items():
        se.flush()
    login_dic.clear()
    return res(10086, "所有人都登出了")


@csrf_exempt
def avatar(request):
    username = request.path.split('/')[-1]
    print(username)

    try:
        user = User.objects.get(username=username)
        return HttpResponse(user.avatar.read(), content_type='image/png')
    except:
        try:
            default_user = User.objects.get(username='default')
            return HttpResponse(default_user.avatar.read(), content_type='image/png')
        except:
            return res(1, '本用户没有头像，default用户又找不见，弄啥嘞')


