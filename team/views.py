import json

from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from utility.utility import *
from team.models import Team
from file.models import File
from user.models import User


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
    # 团队名不可重复
    team_list = Team.objects.filter(team_name=vals['team_name'])
    if len(team_list)>0:
        return res(3001, '团队名不得重复')
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
        manager=User.objects.get(userID=vals['userID']),
        team_root_file=root_file
    )
    team.save()
    root_file.team = team
    root_file.save()
    return res(0, '创建团队成功')


# @csrf_exempt
# def get_myteam


@csrf_exempt
def debug_all_team(request):
    team_list = Team.objects.all()
    result = []
    for team in team_list:
        result.append(team.to_dic())
    return JsonResponse(result,safe=False)


@csrf_exempt
def debug_clear_team(request):
    team_list = Team.objects.all()
    result = []
    for team in team_list:
        team.delete()
    return res(10086, '团队已清空')



