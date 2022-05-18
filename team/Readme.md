# 创建团队

/api/team/create_team

### 需要参数

- team_name

### 返回结果
- 0：创建成功
- 2、3、4：见../Readme.md
- 3001：团队名重复

# 查看用户所在的团队

/api/team/my_team_list

### 需要参数

无

### 返回结果
- 0：成功获取
- 2、3、4：见../Readme.md

# 申请加入团队

/api/team/apply_for_joining_team

### 需要参数

- team_name

### 返回结果
- 0：成功加入团队
- 2、3、4：见../Readme.md
- 3003：用户已经在这个团队中

# 查看团队信息

/api/team/team_info

### 需要参数

- team_name

### 返回结果
- 0：成功加入团队
- 2、3、4：见../Readme.md
- 3002：用户不在这个团队中，无权查看信息

# debug 查看全部团队

/api/team/debug_all_team

获得数据库中全部团队的列表

# debug 删除全部团队

/api/team/debug_clear_team
