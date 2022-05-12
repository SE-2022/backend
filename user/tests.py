from django.test import TestCase, Client
from django.contrib.auth.hashers import make_password, check_password

from user.models import User
from user.views import *
import json

# Create your tests here.

def post_and_loads(client, method_name, dic):
    response = client.post('/api/user/'+method_name, dic)
    return json.loads(response.content)

class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(
            username='a',
            password=make_password('12345678'),
            email='baaabab',
        )
        User.objects.create(
            username='b',
            password=make_password('qwertyui'),
            email='qwererer'
        )
        User.objects.create(
            username='ccc',
            password=make_password('qwertyui'),
            email='cccc@xxx'
        )

    # 登录测试
    def test_login(self):
        c = Client()
        response = c.post('/api/user/login', {'username': 'a', 'password': '12345678'})
        j = json.loads(s=response.content)
        self.assertEqual(j['errno'], 0)
        c.post('/api/user/logout',{})

    # 登出测试
    def test_logout(self):
        c = Client()
        j = post_and_loads(c, 'login', {'username':'b', 'password':'qwertyui'})
        self.assertEqual(j['errno'], 0)
        j = post_and_loads(c, 'logout', {})
        self.assertEqual(j['errno'], 0)

    # 未登录时的方法可用性测试
    def test_not_login_yet(self):
        login_method_list = ['get_user_info', 'edit_user_info', 'logout']
        not_login_method_list = ['login']
        c = Client()
        for method in login_method_list:
            j = post_and_loads(c, method, {})
            self.assertEqual(j['errno'], 3)
        for method in not_login_method_list:
            j = post_and_loads(c, method, {})
            self.assertNotEqual(j['errno'], 3)
        return

    # 登陆后的方法可用性测试
    def test_login_yet(self):
        login_method_list = ['get_user_info', 'edit_user_info', 'logout']
        not_login_method_list = ['login']
        c = Client()
        j = post_and_loads(c, 'login', {'username': 'b', 'password': 'qwertyui'})
        self.assertEqual(j['errno'], 0)
        j = post_and_loads(c, 'debug_status', {})
        # print(j)
        for method in not_login_method_list:
            j = post_and_loads(c, method, {'username': 'a', 'password': 'qwertyui'})
            self.assertEqual(j['errno'], 1011)
            # j = post_and_loads(c, 'debug_status', {})
            # print(j)
        for method in login_method_list:
            j = post_and_loads(c, method, {})
            self.assertNotEqual(j['errno'], 3)

    # 对于缺少字段的覆盖性测试
    def test_lack(self):
        must_exist_list_dic0 = {
            'login': ['username', 'password'],
            'register': ['username', 'password', 'email'],
        }
        must_exist_list_dic1 = {
            'edit_user_info': ['username', 'password', 'email'],
        }
        c = Client()
        try:
            for method in must_exist_list_dic0.keys():
                must_exist_list = must_exist_list_dic0[method]
                dic = {}
                for m in must_exist_list:
                    dic[m] = 0  # 给字典加上每个字段
                for m in must_exist_list:
                    dic.pop(m)  # 删除这个字段
                    j = post_and_loads(c, method, dic)
                    self.assertEqual(j['errno'], 4)
                    dic[m] = 0  # 恢复这个字段
        except AssertionError as ase:
            print('in test_lack of '+method+':\n'+
                  '字段 \''+m+'\' 的缺失没有返回4，而是返回'+str(j['errno']))
        j = post_and_loads(c,'login',{'username': 'b', 'password': 'qwertyui'})
        self.assertEqual(j['errno'],0)
        try:
            for method in must_exist_list_dic1.keys():
                must_exist_list = must_exist_list_dic1[method]
                dic = {}
                for m in must_exist_list:
                    dic[m] = 0  # 给字典加上每个字段
                for m in must_exist_list:
                    dic.pop(m)  # 删除这个字段
                    j = post_and_loads(c, method, dic)
                    self.assertEqual(j['errno'], 4)
                    dic[m] = 0  # 恢复这个字段
        except AssertionError as ase:
            print('in test_lack of '+method+':\n'+
                  '字段 \''+m+'\' 的缺失没有返回4，而是返回'+str(j['errno']))


