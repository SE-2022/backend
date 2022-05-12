# 金刚石文档后端

## 通用错误码

|错误码|  含义  |
|-|--------|
|0| 无错误 |
|1|未知错误，msg应为异常信息 |
|2|请求方式错误 |
|3| 用户未登录，尝试做登录后才能执行的操作 |
|4|请求中缺少字段|

## 目录说明

### 金刚石文档组成部分
- diamond_bg：
- user：用户登录注册、查看修改个人信息
- file：文件管理
- team：团队管理
- message：消息系统

### 其它
- utility：一些小工具，方便代码编写
- upload：上传的头像等媒体文件保存到这里

## django测试方法

以下内容都是lyh在5.12尝试的，不一定正确（

- 测试代码写在每个app文件夹中的tests.py

- tests.py中可以有多个测试类，命名为XXXTestCase

- 每个测试类中写一个setUp方法，和若干个test开头的测试函数

- setUp方法在每个测试函数运行之前都会执行一次

- 运行测试的时候会在一个新的数据库上进行，所以不会受现有数据库的影响（大概


### 例子

```python
# 必须继承TestCase，Client是为了模拟发送request
from django.test import TestCase, Client

from user.models import User
from user.views import *

import json

class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(
            username='a',
            password=make_password('12345678'),
            email='baaabab',
        )

    # 登录测试
    def test_login(self):
        c = Client()
        response = c.post('/api/user/login', {'username': 'a', 'password': '12345678'})
        j = json.loads(s=response.content)
        self.assertEqual(j['errno'], 0)
        c.post('/api/user/logout',{})
```

更多例子见user/tests.py

### 运行测试

#### 全部测试
`python ./manage.py test`

#### 对特定app测试，例如user
`python ./manage.py test user`

    




