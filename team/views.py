import json

from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import *

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
            'create_time': entry.team.create_time.date()}
        team_list.append(t)
    return JsonResponse({'errno': 0, 'msg': '成功获取团队列表', 'team_list': team_list})


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
    vals = post_getAll(request, 'team_name', 'username')
    vals['userID'] = request.session['userID']
    lack, lack_list = check_lack(vals)
    if lack:
        return lack_err(lack_list)
    # 获取用户对象
    found, user = get_user(vals['username'])
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
        return res(3003, "用户 "+vals['username']+" 已经在团队 "+vals['team_name']+" 中")
    # 发出邀请的用户必须是此团队的管理员
    if team.manager.userID != me.userID:
        return res(3004, "目前登录的用户 %s 不是团队 %s 的管理员，只有管理员能发出邀请"
                   % (me.username, vals['team_name']))
    # 检查通过，实施修改
    Team_User.objects.create(team=team, user=user)
    return res(0, "用户 %s 已加入团队 %s" % (vals['username'], vals['team_name']))


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
    username_list = list(map(lambda x: x.user.username, tu_list))
    return JsonResponse({'errno': 0,
                         'msg': '获取团队信息成功',
                         'team_info': {
                             'manager': team.manager.username,
                             'user_list': username_list,
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
