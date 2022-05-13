from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from file.models import File
from team.models import Team
from user.models import User
from user.views import login_check, res


# from file.models import Directory


@csrf_exempt
def personal_filelist(user):
    file_list = File.objects.filter(user=user)
    res = []
    for i in file_list:
        if not i.isDelete:
            res.append({"fileName": i.file_name, "createTime": i.create_time, "lastEditTime": i.last_modify_time})
    return res


@csrf_exempt
def delete_filelist(user):
    file_list = File.objects.filter(user=user)
    res = []
    for i in file_list:
        if i.isDelete:
            res.append({"fileName": i.file_name, "createTime": i.create_time, "lastEditTime": i.last_modify_time})
    return res


# @csrf_exempt
# def get_filelist(request):


@csrf_exempt
def create_file(request):
    if request.method == 'POST':
        if login_check(request):
            try:
                file_name = request.POST.get('file_name')
                user = User.objects.get(userID=request.session['userID'])
                comment = request.POST.get('commentFul')
                file_type = request.POST.get('isDir')
                father_id = request.POST.get('father_id')  # 返回当前文件夹的父节点编号，若当前在根目录下，则返回0
            except ValueError:
                return JsonResponse({'errno': 2001, 'msg': "文件名不得为空"})
            except Exception as e:
                return JsonResponse({'errno': 2000, 'msg': repr(e)})
            file = File.objects.filter(file_name=file_name, isDelete=False)
            if file.count():
                return JsonResponse({'errno': 2002, 'msg': "文件名重复"})
            else:
                username = user.username
                # team = Team.objects.filter(manager=user, isPerson=True)
                # if team.count() == 0:
                #     team = Team(manager=user, isPerson=True)
                #     team.save()
                # else:
                #     team = Team.objects.get(manager=user, isPerson=True)
                new_file = File(fatherID=father_id,
                                # isDir=file_type,
                                file_name=file_name,
                                username=username,
                                user=user,
                                commentFul=comment,
                                # TeamID=team,
                                isDelete=False)
                # How to acquire the directory the file belong to?
                new_file.save()
                result = {'errno': 0,
                          "fileID":new_file.fileID,
                          'fileName': new_file.file_name,
                          'create_time': new_file.create_time,
                          'last_modify_time': new_file.last_modify_time,
                          'commentFul': new_file.commentFul,
                          'isDir': new_file.isDir,
                          'author': new_file.user.username,
                          'msg': "新建成功"}
                return JsonResponse(result)

        else:
            return JsonResponse({'errno': 2009, 'msg': "用户未登录"})
    else:
        return JsonResponse({'errno': 2010, 'msg': "请求方式错误"})


@csrf_exempt
def edit_file(request):
    if not request.method == 'POST':
        return JsonResponse({'errno': 2010, 'msg': "请求方式错误"})
    if not login_check(request):
        return JsonResponse({'errno': 2009, 'msg': "用户未登录"})
    try:
        fileid = request.POST.get('fileid')
        file_content = request.POST.get('file_content')
    except ValueError:
        return JsonResponse({'errno': 2011, 'msg': "无法获取文件信息"})
    except Exception as e:
        return JsonResponse({'errno': 2000, 'msg': repr(e)})

    file = File.objects.get(fileID=fileid)

    if file.isDelete:
        return JsonResponse({'errno': 2012, 'msg': "文件已被删除"})
    elif file.isDir:
        return JsonResponse({'errno': 2013, 'msg': "无法编辑文件夹内容"})
    else:
        file.content = file_content
        file.save()
        result = {'errno': 0,
                  'fileName': file.file_name,
                  'create_time': file.create_time,
                  'last_modify_time': file.last_modify_time,
                  'author': file.user.username,
                  'msg': "保存成功"}
        return JsonResponse(result)


@csrf_exempt
def delete_file(request):
    if request.method == 'POST':
        if login_check(request):
            try:
                file_name = request.POST.get('file_name')

                user = User.objects.get(userID=request.session['userID'])
                # fileid = request.POST.get('fileid')
            except ValueError:
                return JsonResponse({'errno': 2003, 'msg': "文件不存在"})
            except Exception as e:
                return JsonResponse({'errno': 2000, 'msg': repr(e)})

            file = File.objects.get(file_name=file_name, isDelete=False)
            fileid = file.fileID
            file.isDelete = True
            file.save()
            res = {'errno': 0, 'msg': "文档删除成功", 'personal_fileList': personal_filelist(user),
                   'delete_fileList': delete_filelist(user)}
            return JsonResponse(res)
        else:
            return JsonResponse({'errno': 2009, 'msg': "用户未登录"})
    else:
        return JsonResponse({'errno': 2010, 'msg': "请求方式错误"})


@csrf_exempt
def person_root_filelist(request):
    if request.method != 'POST':
        return res(1, '请求方式错误')
    if not login_check(request):
        return res(1006, '用户未登录')
    user = User.objects.get(userID=request.session['userID'])
    if user.root_file is None:
        return res(10086, '此用户没有root文件夹，这种情况不应该出现')
    filelist = File.objects.filter(fatherID=user.root_file.fileID)
    result = []
    for file in filelist:
        result.append(file.to_dic())
    return JsonResponse({'errno': 0, 'msg': '成功获取个人根文件列表',
                         'filelist': result})
