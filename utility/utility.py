from django.http import JsonResponse


# ----------------- 实用小工具 ----------------------

# 检查是否已登录
def login_check(request):
    return 'userID' in request.session


# 能少写几个字母
def res(errno, message):
    return JsonResponse({'errno': errno, "msg": message})


# 一次性get所有参数, args为可变参数列表
def post_getAll(request, *args):
    result = {}
    for arg in args:
        result[str(arg)] = request.POST.get(str(arg))
    return result


# 检查一个字典中是否有none
def check_lack(obj_dic):
    lack_list = []
    for key, obj in obj_dic.items():
        if obj is None:
            lack_list.append(key)
    if len(lack_list) > 0:
        return True, lack_list
    return False, None


# ------------------ 通用异常 -----------------------

# 未甄别的错误，直接返回异常信息
# def unknown_err(exception):
#     return res(1, repr(exception))
# 后来想了想，不如不处理这种异常，直接在前端看见完整的异常信息

def method_err():
    return res(2, '请求方式错误')


def need_login():
    return res(3, '此操作需要登录')


# 传过来的数据存在缺项
def lack_err(lack_list):
    return JsonResponse({
        'errno': 4,
        'msg': '请求缺少字段',
        'lack_list': list(lack_list),
    })
