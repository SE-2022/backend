# publish (unused now)/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from publish.models import Author   # 引入数据库 Author 对象


@csrf_exempt    # 跨域设置
def register(request):  # 继承请求类
    if request.method == 'POST':  # 判断请求方式是否为 POST（此处要求为POST方式）
        username = request.POST.get('username')  # 获取请求体中的请求数据
        password_1 = request.POST.get('password_1')
        password_2 = request.POST.get('password_2')
        if password_1 != password_2:    # 若两次输入的密码不同，则返回错误码errno和描述信息msg
            return JsonResponse({'errno': 1002, 'msg': "两次输入的密码不同"})
        else:
            # 新建 Author 对象，赋值用户名和密码并保存
            new_author = Author(username=username, password=password_1)
            new_author.save()   # 一定要save才能保存到数据库中
            return JsonResponse({'errno': 0, 'msg': "注册成功"})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})


@csrf_exempt    # 跨域设置
def login(request):  # 继承请求类
    if request.method == 'POST':  # 判断请求方式是否为 POST（此处要求为POST方式）
        username = request.POST.get('username')  # 获取请求体中的请求数据
        password = request.POST.get('password')
        if username == 'admin' and password == 'admin':
            return JsonResponse({'errno': 0, 'msg': "登录成功"})
        else:
            return JsonResponse({'errno': 1, 'msg': "用户名密码错误"})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})
