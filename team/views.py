import json

from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import *

from file.views import team_check
from utility.utility import *
from team.models import Team, Team_User
from file.models import File
from user.models import User


# 由团队名得到团队对象
def name2team(team_name):
    try:
        team = Team.objects.get(team_name=team_name)
    except ObjectDoesNotExist:
        return False, res(3001, '团队名 ' + team_name + ' 不存在')
    except MultipleObjectsReturned:
        return False, res(1, '团队名 ' + team_name + ' 被多个团队拥有，' +
                   '不应该出现此情况，请联系lyh')
    return True, team


def name2user(username):
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        return False, res(1, '用户名 '+username+' 不存在')
    except MultipleObjectsReturned:
        return False, res(1, '用户名 ' + username + ' 被多个用户拥有，' +
                   '不应该出现此情况，请联系lyh')
    return True, user


@csrf_exempt
def create_team(request):
    # 一般检查
    if request.method != 'POST':
        return method_err()
    if not login_check(request):
        return need_login()
    # 获取信息，并检查是否缺项
    vals = post_getAll(request, 'team_name')
    vals['userID'] = request.session['userID']
    lack, lack_list = check_lack(vals)
    if lack:
        return lack_err(lack_list)
    # 团队名不可为空
    if len(vals['team_name']) == 0:
        return res(3007, "团队名不能为空")
    # 团队名不可重复
    team_list = Team.objects.filter(team_name=vals['team_name'])
    if len(team_list) > 0:
        return res(3001, '团队名不得重复')
    # 获取本用户
    user= User.objects.get(userID=vals['userID'])
    # 生成团队根文件
    root_file = File(
        fatherID=-1,
        isDir=True,
        file_name='root',
        commentFul=False,
        isDelete=False,
    )
    root_file.save()
    # 设置团队
    team = Team(
        team_name=vals['team_name'],
        manager=user,
        team_root_file=root_file
    )
    team.save()
    root_file.team = team
    root_file.save()
    Team_User.objects.create(user=user, team=team)
    return res(0, '创建团队成功')


# 登录用户获取自己加入了哪些团队
@csrf_exempt
def my_team_list(request):
    # 一般检查
    if request.method != 'POST':
        return method_err()
    if not login_check(request):
        return need_login()
    userID = request.session['userID']
    user = User.objects.get(userID=userID)
    entry_list = Team_User.objects.filter(user=user)
    # print(len(entry_list))
    team_list = []
    for entry in entry_list:
        t = {
            'team_name': entry.team.team_name,
            'manager': entry.team.manager.username,
            'create_time': entry.team.create_time.date(),
            'root_file': entry.team.team_root_file_id}
        team_list.append(t)
    return JsonResponse({'errno': 0,
                         'msg': '成功获取团队列表',
                         'team_list': team_list})


# 通过团队名模糊搜索团队，待实现
@csrf_exempt
def search_team_by_name(request):
    pass


# 申请加入团队，但目前会直接加入那个团队，没有审核步骤
@csrf_exempt
def apply_for_joining_team(request):
    # 一般检查
    if request.method != 'POST':
        return method_err()
    if not login_check(request):
        return need_login()
    # 获取信息，并检查是否缺项
    vals = post_getAll(request, 'team_name')
    vals['userID'] = request.session['userID']
    lack, lack_list = check_lack(vals)
    if lack:
        return lack_err(lack_list)
    # 搜索团队名严格匹配的团队
    success, result = name2team(vals['team_name'])
    if not success:
        return result
    team = result
    # 获取本用户
    user = User.objects.get(userID=vals['userID'])
    # 查找本用户是否已经在此团队中
    if len(Team_User.objects.filter(user=user, team=team)) > 0:
        return res(3003, '用户 {} 已经在团队 {} 中'.format(user.username, team.team_name))
    Team_User.objects.create(user=user, team=team)
    return res(0, '用户 {} 成功加入团队 {}'.format(user.username, team.team_name))


@csrf_exempt
def invite(request):
    # 一般检查
    if request.method != 'POST':
        return method_err()
    if not login_check(request):
        return need_login()
    # 获取信息，并检查是否缺项
    vals = post_getAll(request, 'team_name', 'username_or_email')
    vals['userID'] = request.session['userID']
    lack, lack_list = check_lack(vals)
    if lack:
        return lack_err(lack_list)
    # 获取用户对象
    found, user = get_user(vals['username_or_email'])
    if not found:
        return user
    # 获取团队对象
    try:
        team = Team.objects.get(team_name=vals['team_name'])
    except ObjectDoesNotExist:
        return res(3006, "不存在 "+vals['team_name']+" 这个团队")
    except MultipleObjectsReturned:
        return res(1, "有多个团队具有名称 "+vals['team_name']+" ，这是一个bug")
    # 获取本用户
    me = User.objects.get(userID=vals['userID'])
    # 被邀请的用户不能已经在这个团队中
    if len(Team_User.objects.filter(team=team, user=user)) > 0:
        return res(3003, "用户 "+vals['username_or_email']+" 已经在团队 "+vals['team_name']+" 中")
    # 发出邀请的用户必须是此团队的管理员
    if team.manager.userID != me.userID:
        return res(3004, "目前登录的用户 %s 不是团队 %s 的管理员，只有管理员能发出邀请"
                   % (me.username, vals['team_name']))
    # 检查通过，实施修改
    Team_User.objects.create(team=team, user=user)
    return res(0, "用户 %s 已加入团队 %s" % (vals['username_or_email'], vals['team_name']))


@csrf_exempt
def kick(request):
    # 一般检查
    if request.method != 'POST':
        return method_err()
    if not login_check(request):
        return need_login()
    # 获取信息，并检查是否缺项
    vals = post_getAll(request, 'team_name', 'username_or_email')
    vals['userID'] = request.session['userID']
    lack, lack_list = check_lack(vals)
    if lack:
        return lack_err(lack_list)
    # 获取用户对象
    found, user = get_user(vals['username_or_email'])
    if not found:
        return user
    # 获取团队对象
    try:
        team = Team.objects.get(team_name=vals['team_name'])
    except ObjectDoesNotExist:
        return res(3006, "不存在 "+vals['team_name']+" 这个团队")
    except MultipleObjectsReturned:
        return res(1, "有多个团队具有名称 "+vals['team_name']+" ，这是一个bug")
    # 获取本用户
    me = User.objects.get(userID=vals['userID'])
    # 被踢出的用户必须已经在这个团队中
    team_user = Team_User.objects.filter(team=team, user=user)
    if len(team_user) == 0:
        return res(3003, "用户 "+vals['username_or_email']+" 不在团队 "+vals['team_name']+" 中")
    # 发起踢出的用户必须是此团队的管理员
    if team.manager.userID != me.userID:
        return res(3004, "目前登录的用户 %s 不是团队 %s 的管理员，只有管理员能移除成员"
                   % (me.username, vals['team_name']))
    for tu in team_user:
        tu.delete()
    return res(0, "成员"+user.username+"已被移除")


# 获取团队信息
@csrf_exempt
def team_info(request):
    # 一般检查
    if request.method != 'POST':
        return method_err()
    if not login_check(request):
        return need_login()
    # 获取信息，并检查是否缺项
    vals = post_getAll(request, 'team_name')
    vals['userID'] = request.session['userID']
    lack, lack_list = check_lack(vals)
    if lack:
        return lack_err(lack_list)
    # 获取team
    success, result = name2team(vals['team_name'])
    if not success:
        return result
    team = result
    # 获取user
    user = User.objects.get(userID=vals['userID'])
    # 获取团队用户情况
    tu_list = Team_User.objects.filter(team=team)
    found = False
    for tu in tu_list:
        if tu.user.username == user.username:
            found = True
            break
    if not found:
        return res(3002, '用户 '+user.username+' 不在团队 '+team.team_name+' 中，'+
                   '没有获取信息的权限')
    # username_list = list(map(lambda x: {
    #     'username': x.user.username,
    #     'email': x.user.email,
    # }, tu_list))
    user_list = []
    for tu in tu_list:
        if tu.user.userID != team.manager_id:
            user_list.append({
                'username': tu.user.username,
                'email': tu.user.email,
            })
    manager_list = [{
        'username': team.manager.username,
        'email': team.manager.email,
    }]
    return JsonResponse({'errno': 0,
                         'msg': '获取团队信息成功',
                         'team_info': {
                             'manager_list': manager_list,
                             'user_list': user_list,
                         }})


@csrf_exempt
def debug_all_team(request):
    team_list = Team.objects.all()
    result = []
    for team in team_list:
        result.append(team.to_dic())
    return JsonResponse(result, safe=False)


@csrf_exempt
def debug_clear_team(request):
    team_list = Team.objects.all()
    result = []
    for team in team_list:
        team.delete()
    return res(10086, '团队已清空')


@csrf_exempt
def is_manager(request):
    # 一般检查
    if request.method != 'POST':
        return method_err()
    if not login_check(request):
        return need_login()
    vals = post_getAll(request, 'team_name')
    userID = request.session['userID']
    try:
        team = Team.objects.get(team_name=vals['team_name'])
    except:
        return res(1, "没找到这个团队")
    return JsonResponse({
        'errno': 0,
        'msg': "成功获取成员身份",
        'isManager': team.manager.userID == userID,
    })


# 移交管理权限
@csrf_exempt
def manager_transfer(request):
    # 一般检查
    if request.method != 'POST':
        return method_err()
    if not login_check(request):
        return need_login()
    vals = post_getAll(request, 'username', 'team_name')
    lack, lack_list = check_lack(vals)
    if lack:
        return lack_err(lack_list)
    userID = request.session['userID']
    success, team = name2team(vals['team_name'])
    if not success:
        return team
    success, new_manager = name2user(vals['username'])
    if not success:
        return new_manager
    user = User.objects.get(userID=userID)
    if team.manager.userID != user.userID:
        return res(1, '您不是此团队的管理员，不能移交管理权')
    found = Team_User.objects.filter(team=team, user=new_manager)
    if len(found) == 0:
        return res(1, '用户'+new_manager+'不是团队'+team.team_name+'的成员')
    # 通过检查，实施修改
    team.manager = new_manager
    team.save()
    return res(0, '成功将团队'+team.team_name+'的管理员设为用户'+new_manager.username)


@csrf_exempt
def destroy(request):
    # 一般检查
    if request.method != 'POST':
        return method_err()
    if not login_check(request):
        return need_login()
    vals = post_getAll(request, 'team_name')
    lack, lack_list = check_lack(vals)
    if lack:
        return lack_err(lack_list)
    userID = request.session['userID']
    success, team = name2team(vals['team_name'])
    if not success:
        return team
    user = User.objects.get(userID=userID)
    if team.manager.userID != user.userID:
        return res(1, '您不是此团队的管理员，不能销毁此团队')
    # 通过检查，实施修改
    name = team.team_name
    team.delete()
    return res(0, '团队'+name+'已被销毁')


@csrf_exempt
def rename(request):
    # 一般检查
    if request.method != 'POST':
        return method_err()
    if not login_check(request):
        return need_login()
    vals = post_getAll(request, 'team_name', 'new_team_name')
    lack, lack_list = check_lack(vals)
    if lack:
        return lack_err(lack_list)
    userID = request.session['userID']
    # user = User.objects.get(userID=userID)
    success, team = name2team(vals['team_name'])
    if not success:
        return team
    if team.manager.userID != userID:
        return res(1, '你不是这个团队的管理员，不能修改团队名')
    team_list = Team.objects.filter(team_name=vals['new_team_name'])
    if len(team_list)>0:
        return res(1, '团队名'+vals['new_team_name']+'已被其它团队使用')
    team.team_name = vals['new_team_name']
    team.save()
    return res(0, '团队已改名为'+vals['new_team_name'])


@csrf_exempt
def leave_team(request):
    # 一般检查
    if request.method != 'POST':
        return method_err()
    if not login_check(request):
        return need_login()
    vals = post_getAll(request, 'team_name')
    lack, lack_list = check_lack(vals)
    if lack:
        return lack_err(lack_list)
    success, team = name2team(vals['team_name'])
    if not success:
        return team
    user = User.objects.get(userID=request.session['userID'])
    team_user = Team_User.objects.filter(team=team, user=user)
    if len(team_user) != 1:
        return res(1, '你不是这个团队的成员，无法退出')
    team_user = team_user[0]
    if user.userID == team_user.team.manager.userID:
        return res(1, '您是团队'+vals['team_name']+'的管理员，需要先移交管理权限再退出')
    team_user.delete()
    return res(0, '已退出团队'+vals['team_name'])


# 管理员修改团队文件权限
@csrf_exempt
def modify_team_file_perm(request):
    if not request.method == 'POST':
        return JsonResponse({'errno': 2010, 'msg': "请求方式错误"})
    if not login_check(request):
        return JsonResponse({'errno': 2009, 'msg': "用户未登录"})
    user = User.objects.get(userID=request.session['userID'])
    try:
        file = File.objects.get(fileID=request.POST['fileid'])
    except:
        return res(1, '无法找到这个文件')
    try:
        perm = int(request.POST['perm'])
    except:
        return res(1, "权限必须为0（读写）或1（只读），您提供了" + str(request.POST['perm']))
    good, result = team_check(request)
    if not good:
        return result
    if file.team is None:
        return res(2105, "此文件不是团队文件")
    if file.team.manager.userID != user.userID:
        return res(2106, "需要修改权限请联系团队管理员 " + file.team.manager.username)
    if perm != 0 and perm != 1:
        return res(2107, "权限必须为0（读写）或1（只读），您提供了" + str(perm))
    file.team_perm = perm
    file.save()
    return res(0, "成功修改权限")

# @csrf_exempt
# def set_perm(request):
#     # 一般检查
#     if request.method != 'POST':
#         return method_err()
#     if not login_check(request):
#         return need_login()
#     vals = post_getAll(request, 'fileID', 'perm')
#     lack, lack_list = check_lack(vals)
#     if lack:
#         return lack_err(lack_list)
#     if vals['perm'] != 0 and vals['perm'] != 1:
#         return res(1, '非法perm')
#     try:
#         file = File.objects.get(fileID=vals['fileID'])
#     except:
#         return res(1, '无法找到此文件')
#     if file.team is None:
#         return res(1, '此文件不属于任何团队，无法设置权限')
#     user = User.objects.get(userID=request.session['userID'])
#     if file.team.manager != user:
#         return res(1, '你不是此文件所属团队的管理员')
#     file.team_perm =
