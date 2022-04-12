# saving/views.py
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from saving.models import Article   # 引入数据库 Author 对象


# Create your views here.
@csrf_exempt    # 跨域设置
def save(request):  # 继承请求类
    if request.method == 'POST':  # 判断请求方式是否为 POST（此处要求为POST方式）
        name = request.POST.get('name')  # 获取请求体中的请求数据
        raw = request.POST.get('raw')
        # body = json.loads(request.body)
        # name = body['name']
        # raw = body['raw']
        try:
            file = Article.objects.get(name=name)
            file.raw = raw
            file.save()
        except Article.DoesNotExist:
            Article.objects.create(name=name, raw=raw)
        return JsonResponse({'errno': 0, 'msg': "保存成功"})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})


@csrf_exempt    # 跨域设置
def load(request):  # 继承请求类
    if request.method == 'POST':  # 判断请求方式是否为 POST（此处要求为POST方式）
        name = request.POST.get('name')  # 获取请求体中的请求数据
        try:
            file = Article.objects.get(name=name)
            return JsonResponse({'errno': 0, 'msg': "读取成功", 'name': name, 'raw': file.raw})
        except Article.DoesNotExist:
            return JsonResponse({'errno': 1, 'msg': "文件不存在", 'name': name})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})

@csrf_exempt
def getFileList(request):
    if request.method == 'POST':
        fileList = []
        all = Article.objects.all()
        print(type(all))
        for one in all:
            file = {}
            file['fileName'] = one.name;
            file['createTime'] = one.createTime;
            file['lastEditTime'] = one.lastEditTime;
            fileList.append(file)
        print(fileList)
        return JsonResponse({'errno':0, 'fileList':fileList})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})

def delete(request):

