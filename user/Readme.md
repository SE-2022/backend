# user

## 错误码汇总

|错误码|详情|
|---|---|
|1000|成功|
|1001|未甄别的错误|
|1002|请求缺少字段|
|1003|注册，密码太弱|
|1004|登陆，用户名不存在|
|1005|登陆，密码错误|
|1006|未登录|
|1007|编辑个人信息失败|
|1008|编辑个人头像失败|
|1009|注册，用户名已被注册|
|1010|编辑个人信息，用户名已存在|

## 路由

前缀为api/user/
- 注册：register
- 登录：login
- 注销：logout
- 等等

## 其它值得说明的

`request.session`能够确定唯一的“服务器-浏览器”会话，这是由django保证的，可能是靠cookie

`request.session`的操作方式类似于python的字典，对这个对象的写操作会反映在数据库的session表中

在`login`方法中，`request.session['userID']`被设为`userID`

在`logout`方法中，会调用`request.session.flush()`方法，大概会把字典清空

其它函数可据此判断是否登录，以及登录者是谁，`user/views.py`也提供了`login_check(request)`函数