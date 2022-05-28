from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from file.models import File, Comment
from team.models import Team, Team_User
from user.models import User
from user.views import login_check, res
import qrcode

# from file.models import Directory


@csrf_exempt
def acquire_filelist(user, father_id, allow_del):
    file_list = File.objects.filter(user=user, fatherID=father_id)
    result = []
    for i in file_list:
        if not (i.isDelete and not allow_del):
            result.append({"fileID": i.fileID, "fileName": i.file_name, "createTime": i.create_time,
                           "lastEditTime": i.last_modify_time,
                           "isDir": i.isDir, "fatherID": i.fatherID})
    return result


@csrf_exempt
def delete_filelist(user):
    file_list = File.objects.filter(user=user, isDelete=True, fatherID=user.root_file.fileID)
    result = []
    for i in file_list:
        # # if i.isDelete:
        # if not i.isDir:
        #     father_id = i.fatherID
        #     father_file = File.objects.get(fileID=father_id)
        #     if not father_file.isDelete:
        #         result.append({"fileID": i.fileID, "fileName": i.file_name, "createTime": i.create_time,
        #                        "lastEditTime": i.last_modify_time,
        #                        "fatherID": i.fatherID,
        #                        "isDir": i.isDir})
        #     else:
        #         f_del_time = father_file.last_modify_time
        #         del_time = i.last_modify_time
        #         if del_time >= f_del_time:
        #             result.append({"fileID": i.fileID, "fileName": i.file_name, "createTime": i.create_time,
        #                            "lastEditTime": i.last_modify_time,
        #                            "fatherID": i.fatherID,
        #                            "isDir": i.isDir})
        # (i.fatherID == user.root_file.fileID or (not File.objects.get(
        # fileID=i.fatherID).isDelete) or (File.objects.get(
        # fileID=i.fatherID).isDelete and File.objects.get(
        # fileID=i.fatherID).last_modify_time > i.last_modify_time)):  # 仅显示root文件夹下被删除的文件与文件夹
        # if i.fatherID == user.root_file.fileID:
        result.append({"fileID": i.fileID, "fileName": i.file_name, "createTime": i.create_time,
                       "lastEditTime": i.last_modify_time,
                       "fatherID": i.fatherID,
                       "isDir": i.isDir})
        # elif not File.objects.get(fileID=i.fatherID).isDelete:
        # result.append({"fileID": i.fileID, "fileName": i.file_name, "createTime": i.create_time,
        #                "lastEditTime": i.last_modify_time,
        #                "fatherID": i.fatherID,
        #                "isDir": i.isDir})
    # elif File.objects.get(fileID=i.fatherID).last_modify_time > i.last_modify_time:
    #     result.append({"fileID": i.fileID, "fileName": i.file_name, "createTime": i.create_time,
    #                    "lastEditTime": i.last_modify_time,
    #                    "fatherID": i.fatherID,
    #                    "isDir": i.isDir})

    return result


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
            file = File.objects.filter(file_name=file_name, isDelete=False, user=user)
            # if file.count():
            #     return JsonResponse({'errno': 2002, 'msg': "文件名重复"})
            # else:
            username = user.username
            new_file = File(fatherID=father_id,
                            isDir=file_type,
                            file_name=file_name,
                            username=username,
                            user=user,
                            commentFul=comment,
                            # TeamID=team,
                            isDelete=False)
            # How to acquire the directory the file belong to?
            new_file.save()
            result = {'errno': 0,
                      "fileID": new_file.fileID,
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
def read_file(request):
    if not request.method == 'POST':
        return JsonResponse({'errno': 2010, 'msg': "请求方式错误"})
    if not login_check(request):
        return JsonResponse({'errno': 2009, 'msg': "用户未登录"})
    try:
        fileid = request.POST.get('fileid')
    except ValueError:
        return JsonResponse({'errno': 2022, 'msg': "获取文件信息失败，无法查看文件内容"})

    file = File.objects.get(fileID=fileid, user=User.objects.get(userID=request.session['userID']))
    if file.isDir:
        return JsonResponse({'errno': 2023, 'msg': "不支持阅读文件夹内容"})
    if file.isDelete:
        return JsonResponse({'errno': 2024, 'msg': "文件已被删除"})

    result = {'errno': 0,
              'fileName': file.file_name,
              'create_time': file.create_time,
              'last_modify_time': file.last_modify_time,
              'author': file.user.username,
              'file_content': file.content,
              'msg': '成功打开文件' + file.file_name,
              }
    return JsonResponse(result)


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
    user = User.objects.get(userID=request.session['userID'])
    file = File.objects.get(fileID=fileid, user=user)

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
def change_file_name(request):
    if not request.method == 'POST':
        return JsonResponse({'errno': 2010, 'msg': "请求方式错误"})
    if not login_check(request):
        return JsonResponse({'errno': 2009, 'msg': "用户未登录"})
    try:
        fileid = request.POST.get('fileid')
        new_name = request.POST.get('newname')
    except ValueError:
        return JsonResponse({'errno': 2025, 'msg': "文件名不得为空"})
    except Exception as e:
        return JsonResponse({'errno': 2000, 'msg': repr(e)})
    user = User.objects.get(userID=request.session['userID'])
    file = File.objects.get(fileID=fileid, user=user)
    file_tmp = File.objects.filter(file_name=new_name, isDelete=False, isDir=file.isDir, user=user)
    if new_name != file.file_name and file_tmp.count() >= 1:
        return JsonResponse({'errno': 2026, 'msg': "文件名重复"})
    file.file_name = new_name
    file.save()
    result = {'errno': 0,
              'fileName': file.file_name,
              'create_time': file.create_time,
              'last_modify_time': file.last_modify_time,
              'author': file.user.username,
              'msg': "修改成功"
              }
    return JsonResponse(result)


@csrf_exempt
def delete_file(request):
    if request.method == 'POST':
        if login_check(request):
            try:
                # file_name = request.POST.get('file_name')
                fileid = request.POST.get('fileid')
            except ValueError:
                return JsonResponse({'errno': 2003, 'msg': "文件不存在"})
            except Exception as e:
                return JsonResponse({'errno': 2000, 'msg': repr(e)})
            user = User.objects.get(userID=request.session['userID'])
            file = File.objects.get(fileID=fileid, user=user)
            if file.isDelete:
                return JsonResponse({'errno': 2004, 'msg': "文件已被删除"})
            else:
                if file.isDir:
                    father = file.fileID  # 记录当前文件夹id,遍历以此为父文件夹的文件并删除
                    delete_dir(user, father)
                file.fatherID = user.root_file.fileID
                file.isDelete = True
                file.save()
                result = {'errno': 0, 'msg': "文档删除成功",
                          'personal_fileList': acquire_filelist(user, user.root_file.fileID, False),
                          'delete_fileList': delete_filelist(user)}
                return JsonResponse(result)
        else:
            return JsonResponse({'errno': 2009, 'msg': "用户未登录"})
    else:
        return JsonResponse({'errno': 2010, 'msg': "请求方式错误"})


def delete_dir(user, file_id):
    """This function is designed to delete directories recursively.
        pre-condition: file_id is the 'fileID' of the directory to be deleted.
        post-condition: Subfiles of the directory will be deleted recursively.
    """
    file = File.objects.get(fileID=file_id, user=user)
    if not file.isDir:
        return JsonResponse({'errno': 2014, 'msg': "无法删除非文件夹内容"})
    file_subset = File.objects.filter(user=user, fatherID=file_id)
    for i in file_subset:
        if i.isDir:
            f = i.fileID
            delete_dir(user, f)
        i.isDelete = True
        i.save()


def completely_delete_dir(user, file_id):
    file = File.objects.get(fileID=file_id, user=user)
    if not (file.isDir and file.isDelete):
        return JsonResponse({'errno': 2019, 'msg': "无法彻底删除"})
    file_subset = File.objects.filter(user=user, fatherID=file_id)
    for i in file_subset:
        if i.isDir:
            f = i.fileID
            completely_delete_dir(user, f)
        i.delete()


@csrf_exempt
def person_root_filelist(request):
    if request.method != 'POST':
        return res(1, '请求方式错误')
    if not login_check(request):
        return res(1006, '用户未登录')
    user = User.objects.get(userID=request.session['userID'])
    if user.root_file is None:
        return res(10086, '此用户没有root文件夹，这种情况不应该出现')
    # filelist = File.objects.filter(fatherID=user.root_file.fileID, isDelete=False)
    # result = []
    # for file in filelist:
    #     result.append(file.to_dic())
    return JsonResponse({'errno': 0, 'msg': '成功获取个人根文件列表', 'root_id': user.root_file.fileID,
                         'filelist': acquire_filelist(user, user.root_file.fileID, False)})


@csrf_exempt
def get_file_list_of_dir(request):
    """
        This function is designed for looking up the filelist of a specific directory based on the fileID of it.
        Tip: Directories in the recycle bin can be looked up as well.
    """
    if request.method == 'POST':
        if not login_check(request):
            return JsonResponse({'errno': 2009, 'msg': "用户未登录"})
        try:
            father_id = request.POST.get('fatherID')
        except ValueError:
            return JsonResponse({'errno': 2015, 'msg': "父文件夹信息获取失败"})
        except Exception as e:
            return JsonResponse({'errno': 2000, 'msg': repr(e)})
        user = User.objects.get(userID=request.session['userID'])
        father_dir = File.objects.get(fileID=father_id, user=user)
        # if father_dir.isDelete:
        #     return JsonResponse({'errno': 2016, 'msg': "文件夹已被删除"})
        if not father_dir.isDir:
            return JsonResponse({'errno': 2017, 'msg': "无法查看非文件夹内容"})
        else:
            if father_dir.isDelete:
                result = {'errno': 0, 'msg': "打开文件夹成功", 'dir_filelist': acquire_filelist(user, father_id, True)}
            else:
                result = {'errno': 0, 'msg': "打开文件夹成功", 'dir_filelist': acquire_filelist(user, father_id, False)}
            return JsonResponse(result)

    else:
        return JsonResponse({'errno': 2010, 'msg': "请求方式错误"})


@csrf_exempt
def get_filelist_of_recycle_bin(request):
    """return filelist in the recycle bin"""
    if request.method == 'POST':
        if not login_check(request):
            return JsonResponse({'errno': 2009, 'msg': "用户未登录"})
        user = User.objects.get(userID=request.session['userID'])
        return JsonResponse({'errno': 0, 'msg': "成功打开回收站", 'delete_fileList': delete_filelist(user)})
    else:
        return JsonResponse({'errno': 2010, 'msg': "请求方式错误"})


@csrf_exempt
def completely_delete_file(request):
    if request.method == 'POST':
        if not login_check(request):
            return JsonResponse({'errno': 2009, 'msg': "用户未登录"})
        try:
            fileid = request.POST.get('fileid')
        except ValueError:
            return JsonResponse({'errno': 2018, 'msg': "文件信息获取失败"})
        except Exception as e:
            return JsonResponse({'errno': 2000, 'msg': repr(e)})
        user = User.objects.get(userID=request.session['userID'])
        file = File.objects.get(fileID=fileid, user=user)
        if not file.isDelete:
            return JsonResponse({'errno': 2019, 'msg': "文件未删除，无法执行彻底删除操作"})
        if file.isDir:
            father = file.fileID
            completely_delete_dir(user, father)
        file.delete()
        result = {'errno': 0, 'msg': "彻底删除成功",
                  # 'personal_fileList': acquire_filelist(user, user.root_file.fileID),
                  'delete_fileList': delete_filelist(user)}
        return JsonResponse(result)

    else:
        return JsonResponse({'errno': 2010, 'msg': "请求方式错误"})


def restore_dir(user, fileid):
    file = File.objects.get(fileID=fileid, user=user)
    if not (file.isDir and file.isDelete):
        return
    file_subset = File.objects.filter(user=user, fatherID=fileid, isDelete=True)
    for i in file_subset:
        if i.isDir:
            restore_dir(user, i.fileID)
        i.isDelete = False
        i.save()


@csrf_exempt
def restore_file(request):
    """This function is designed for restoring files which have been put into the recycle bin.
        After restoring, the file/directory will be placed in the root filelist whatever its father directory used to be.
    """
    if request.method == 'POST':
        if not login_check(request):
            return JsonResponse({'errno': 2009, 'msg': "用户未登录"})
        try:
            fileid = request.POST.get('fileid')
        except ValueError:
            return JsonResponse({'errno': 2020, 'msg': "无法获取文件信息"})
        except Exception as e:
            return JsonResponse({'errno': 2000, 'msg': repr(e)})

        user = User.objects.get(userID=request.session['userID'])
        file = File.objects.get(fileID=fileid, user=user)
        if not file.isDelete:
            return JsonResponse({'errno': 2021, 'msg': "文件不在回收站中"})
        if file.isDir:
            restore_dir(user, fileid)
        file.isDelete = False
        file.save()
        result = {'errno': 0, 'msg': "文件恢复成功",
                  # 'personal_fileList': acquire_filelist(user, user.root_file.fileID),
                  'delete_fileList': delete_filelist(user)}
        return JsonResponse(result)
    else:
        return JsonResponse({'errno': 2010, 'msg': "请求方式错误"})


# 所有访问文件的操作都需要进行此检查
# 估计要塞到文件这边的所有函数里面
def team_check(request):
    fileid = request.POST.get('fileid')
    if fileid is None:  # 没有fileid字段？
        return True, None
    # 获得file对象
    try:
        file = File.objects.get(fileID=fileid)
    except:  # 本函数不管这种情况
        return True, None
    # 检查file是否属于团队
    if file.team is None:
        return True, None
    # 获得user对象
    userID = request.session.get['userID']
    user = User.objects.get(userID=userID)
    # 检查user是否属于file所在的团队
    try:
        Team_User.objects.get(team=file.team, user=user)
    except ObjectDoesNotExist:
        return False, res(2101, "此文件属于某个团队，而您不是这个团队的成员")
    except:
        return False, res(1, "不应该出这个问题")
    return True, None


# 创建团队文件，是在函数create_file的基础上修改，还是重写一个？
@csrf_exempt
def create_team_file(request):
    pass


@csrf_exempt
def set_comment_to(request):
    if request.method == 'POST':
        if not login_check(request):
            return JsonResponse({'errno': 2009, 'msg': "用户未登录"})
        try:
            fileid = request.POST.get('fileid')
        except ValueError:
            return JsonResponse({'errno': 2027, 'msg': "无法获取文件信息"})
        user = User.objects.get(userID=request.session['userID'])
        try:
            file = File.objects.get(fileID=fileid, isDelete=False, isDir=False)
        except ObjectDoesNotExist:
            return JsonResponse({'errno': 2028, 'msg': "文件不存在"})
        if not file.commentFul:
            return JsonResponse({'errno': 2029, 'msg': "该文章不可评论哟～"})

        comment_content = request.POST.get('comment_content')
        if comment_content is None:
            return JsonResponse({'errno': 2030, 'msg': "评论内容不得为空"})
        comment = Comment(content=comment_content, comment_fileID=file, comment_user=user)
        comment.save()
        return JsonResponse(
            {'errno': 0, 'msg': "感谢您的评论", 'commentID': comment.commentID, 'comment_time': comment.comment_time,
             'content': comment.content, 'commenter': comment.comment_user.username})
    else:
        return JsonResponse({'errno': 2010, 'msg': "请求方式错误"})


@csrf_exempt
def change_comment_character(request):
    if request.method == 'POST':
        if not login_check(request):
            return JsonResponse({'errno': 2009, 'msg': "用户未登录"})
        try:
            fileid = request.POST.get('fileid')
            new_state = request.POST.get('commentFul')
        except ValueError:
            return JsonResponse({'errno': 2031, 'msg': "获取信息失败"})
        user = User.objects.get(userID=request.session['userID'])
        try:
            file = File.objects.get(fileID=fileid, user=user, isDelete=False, isDir=False)
        except ObjectDoesNotExist:
            return JsonResponse({'errno': 2032, 'msg': "文件不存在"})
        if file.commentFul == new_state:
            if new_state:
                return JsonResponse({'errno': 2033, 'msg': "评论功能已开启"})
            else:
                return JsonResponse({'errno': 2034, 'msg': "评论功能已关闭"})
        file.commentFul = new_state
        file.save()
        return JsonResponse({'errno': 0, 'msg': "修改成功"})
    else:
        return JsonResponse({'errno': 2010, 'msg': "请求方式错误"})


@csrf_exempt
def delete_comment(request):
    if request.method == 'POST':
        if not login_check(request):
            return JsonResponse({'errno': 2009, 'msg': "用户未登录"})
        user = User.objects.get(userID=request.session['userID'])
        try:
            comment_id = request.POST.get('comment_id')
            comment = Comment.objects.get(commentID=comment_id)
        except ObjectDoesNotExist:
            return JsonResponse({'errno': 2035, 'msg': "无法获取评论信息"})
        if user == comment.comment_fileID.user or user == comment.comment_user:
            comment.delete()
            return JsonResponse({'errno': 0, 'msg': "删除成功"})
        else:
            return JsonResponse({'errno': 2036, 'msg': "您无法删除该评论"})
    else:
        return JsonResponse({'errno': 2010, 'msg': "请求方式错误"})


@csrf_exempt
def show_comment_list(request):
    if request.method == 'POST':
        # if not login_check(request):
        #     return JsonResponse({'errno': 2009, 'msg': "用户未登录"})
        # user = User.objects.get(userID=request.session['userID'])
        try:
            fileid = request.POST.get('fileid')
            file = File.objects.get(fileID=fileid, isDelete=False, isDir=False)
        except ObjectDoesNotExist:
            return JsonResponse({'errno': 2037, 'msg': "无法获取文件信息"})
        comment_list = Comment.objects.filter(comment_fileID=file)
        comments = []
        for i in comment_list:
            comments.append({'commentID': i.commentID, 'comment_time': i.comment_time,
                             'content': i.content, 'commenter': i.comment_user.username})
        return JsonResponse({'errno': 0, 'comment_list': comments})
    else:
        return JsonResponse({'errno': 2010, 'msg': "请求方式错误"})
