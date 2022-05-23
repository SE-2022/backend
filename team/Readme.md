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
- username：对方的用户名

### 返回结果

| errno | 含义                   |
|-------|----------------------|
| 0     | 成功                   |
|2、3、4| 见../Readme.md        |
|3003| 用户已经在这个团队中           |
|3004| 发出邀请的用户不是本团队管理员，邀请无效 |
|3005| 不存在这个用户名             |
|3006| 不存在这个团队              |

# 查看团队信息

`/api/team/team_info`

### 需要参数

- team_name

### 返回结果
| errno | 含义 |
|-------|----|
| 0     | 成功 |
|2、3、4|见../Readme.md|
|3002|用户不在这个团队中，无权查看信息|

# debug 查看全部团队

`/api/team/debug_all_team`

获得数据库中全部团队的列表

# debug 删除全部团队

`/api/team/debug_clear_team`
