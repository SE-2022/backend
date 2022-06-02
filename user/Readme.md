# user

## 注册

`/api/user/register`

### 需要参数
- username
- password
- email

### 返回结果

| errno | 含义            |
|-------|---------------|
| 0     | 成功            |
|2、3、4| 见../Readme.md |
|1009| 用户名已被注册       |
|1003| 密码太弱（长度要至少8位） |
|1012| 用户根文件夹创建失败    |
|1013|邮箱已被注册|

## 登录

`/api/user/login`

### 需要参数

- username
- password

### 返回结果

| errno | 含义                       |
|-------|--------------------------|
| 0     | 成功                       |
| 2、3、4 | 见../Readme.md            |
| 1004  | 用户名不存在                   |
| 1001  | 数据库中存在多个相同的用户名，说明后端存在bug |
| 1005  | 密码错误                     |

## 登出

`/api/user/logout`

### 需要参数

无

### 返回结果

| errno | 含义                       |
|-------|--------------------------|
| 0     | 成功                       |
| 2、3、4 | 见../Readme.md            |

## 查看个人信息

`/api/user/get_user_info`

### 需要参数

无

### 返回结果

| errno | 含义                       |
|-------|--------------------------|
| 0     | 成功                       |
| 2、3、4 | 见../Readme.md            |

正确结果栗子
```json
{
    "errno": 0,
    "msg": "获取个人信息成功",
    "user_info": {
        "userID": 6,
        "username": "xyzttt",
        "email": "kjsdhfkjhd"
    }
}
```

# 修改个人信息

`/api/user/edit_user_info`

### 需要参数

- username
- password
- email

### 返回结果

| errno | 含义                       |
|-------|--------------------------|
| 0     | 成功                       |
| 2、3、4 | 见../Readme.md            |
|1007| 个人信息填写有误，可能是有空项或者密码太弱|
|1010|此用户名已经被其他人注册|

正确结果栗子：
```json
{
    "errno": 0,
    "msg": "编辑个人信息成功"
}
```

## 其它值得说明的

`request.session`能够确定唯一的“服务器-浏览器”会话，这是由django保证的，可能是靠cookie

`request.session`的操作方式类似于python的字典，对这个对象的写操作会反映在数据库的session表中

在`login`方法中，`request.session['userID']`被设为`userID`

在`logout`方法中，会调用`request.session.flush()`方法，大概会把字典清空

其它函数可据此判断是否登录，以及登录者是谁，`user/views.py`也提供了`login_check(request)`函数