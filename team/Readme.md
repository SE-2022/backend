# 创建团队

/api/team/create_team

### 需要参数

- team_name

### 返回结果
- 0：创建成功
- 2、3、4：见../Readme.md
- 3001：团队名重复
- 3007：团队名不能为空

# 查看用户所在的团队

`/api/team/my_team_list`

### 需要参数

无

### 返回结果

| errno | 含义      |
|-------|---------|
| 0     | 成功      |
|2、3、4| 见../Readme.md |


# 申请加入团队

`/api/team/apply_for_joining_team`

### 需要参数

- team_name

### 返回结果

| errno | 含义 |
|-------|----|
| 0     | 成功 |
|2、3、4|见../Readme.md|
|3003|用户已经在这个团队中|

# 邀请

`/api/team/invite`

### 需要参数

- team_name
- username_or_email：对方的用户名或邮箱

### 返回结果

| errno | 含义                   |
|-------|----------------------|
| 0     | 成功                   |
|2、3、4| 见../Readme.md        |
|3003| 用户已经在这个团队中           |
|3004| 发出邀请的用户不是本团队管理员，邀请无效 |
|3005| 不存在这个用户名             |
|3006| 不存在这个团队              |

# 踢出

`/api/team/kick`

### 需要参数

- team_name
- username：对方的用户名

### 返回结果

- 团队不存在
- 你不是管理员
- 团队中没有该成员 

正确结果：

```json
{
    "errno": 0,
    "msg": "已踢出xyz"
}
```

# 查看团队详细信息

`/api/team/team_info`

### 需要参数

- team_name

### 返回结果
| errno | 含义 |
|-------|----|
| 0     | 成功 |
|2、3、4|见../Readme.md|
|3001| 团队名不存在 |
|3002|用户不在这个团队中，无权查看信息|

正确结果栗子：
```json
{
    "errno": 0,
    "msg": "获取团队信息成功",
    "team_info": {
        "manager_list": [
            {
                "username": "xyzttt",
                "email": "kjsdhfkjhd"
            }
        ],
        "user_list": [
            {
                "username": "xyzttt",
                "email": "kjsdhfkjhd"
            },
            {
                "username": "lyh",
                "email": "lyh.net"
            }
        ]
    }
}
```

# 创建团队文件

`/api/file/newteamfile`

### 需要参数

- file_name：字符串，要创建的文件名
- commentFul：布尔值，能否评论
- isDir：布尔值，是不是文件夹
- father_id：数字，父文件夹id
- team_name：字符串，团队名

### 返回结果

| 错误码 | 错误类型                         |
| ------ |------------------------------|
|2101| 试图访问团队文件，但用户不属于这个团队          |
|2108| 创建团队文件，父文件不属于此团队|
|2109| 创建团队文件，但给出了错误的团队名|

正确返回结果例子：
```json
{
    "errno": 0,
    "fileID": 41,
    "fileName": "subLinguisitic3",
    "create_time": "2022-05-29T15:07:30.305Z",
    "last_modify_time": "2022-05-29T15:07:30.305Z",
    "commentFul": "True",
    "isDir": "False",
    "author": "xyz",
    "team": "love and peace",
    "msg": "新建成功"
}
```

# 获取团队根文件列表

`/api/file/team_root_filelist`

### 需要参数

- team_name：字符串，团队名

### 返回结果

瞎写的，errno非0即为错误

正确返回结果例子：
```json
{
    "errno": 0,
    "msg": "成功获取团队根文件列表",
    "root_id": 38,
    "filelist": [
        "subLinguisitic3"
    ]
}
```

# 移交团队管理权限

`/api/team/manager_transfer`

### 需要参数

- team_name：要移交哪个团队的权限
- username：要移交权限给哪个用户

### 返回结果

errno非0即为发生错误，错误可能包括：
- 团队名不存在
- 用户名不存在
- 本用户并非此团队管理员
- 待移交用户并非此团队的成员

正确结果：
```json
{
    "errno": 0,
    "msg": "成功将团队 love and peace 的管理权移交给用户 xyz"
}
```

# 销毁团队

`/api/team/destroy`

### 需要参数

- team_name：要销毁的团队

### 返回结果

errno非0即为发生错误，错误可能包括：
- 团队名不存在
- 本用户并非此团队管理员

正确结果：
```json
{
    "errno": 0,
    "msg": "团队 love and peace 已被销毁"
}
```

# debug 查看全部团队

`/api/team/debug_all_team`

获得数据库中全部团队的列表

# debug 删除全部团队

`/api/team/debug_clear_team`
