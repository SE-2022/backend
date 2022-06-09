# 10个最近浏览的文件

`/api/file/last_10_read_file`

只用于自己创建的个人文件，返回结果中只有文件没有文件夹，不包含已删除的文件

如果找不到10个文件，有几个就返回几个

”最近浏览时间“在调用read_file的时候会刷新成当前时间

### 需要参数

不需要参数

### 返回结果

没有特别的错误

正确结果：
```json
{
    "errno": 0,
    "msg": "成功获取3个最近访问的文件",
    "file_list": [
        {
            "fileID": 43,
            "fileName": "？",
            "createTime": "2022-06-08T17:10:50.391Z",
            "lastEditTime": "2022-06-08T17:14:16.656Z",
            "lastReadTime": "2022-06-08T17:14:16.656Z",
            "isDir": false,
            "fatherID": 6,
            "is_fav": false
        },
        {
            "fileID": 44,
            "fileName": "？？",
            "createTime": "2022-06-08T17:10:53.771Z",
            "lastEditTime": "2022-06-08T17:14:07.816Z",
            "lastReadTime": "2022-06-08T17:14:07.816Z",
            "isDir": false,
            "fatherID": 6,
            "is_fav": false
        },
        {
            "fileID": 42,
            "fileName": "subLinguisitic3",
            "createTime": "2022-06-08T17:10:34.654Z",
            "lastEditTime": "2022-06-08T17:10:34.654Z",
            "lastReadTime": "2022-06-08T17:10:34.654Z",
            "isDir": false,
            "fatherID": 6,
            "is_fav": false
        }
    ]
}
```


# 生成分享链接

`/api/file/create_share_link`

只有自己创建的个人文件能生成分享链接

### 需要参数

- fileID：分享哪个文件
- perm：以什么权限分享，0读写，1只读

### 返回结果

可能的错误：
- 你不是这个文件的创建者
- 这是团队文件，不能分享
- perm不对

正确结果：
```json
{
    "errno": 0,
    "res": "成功生成分享链接",
    "link": "http://123.57.69.30/api/link/sVUZT5P6ZmUWMy3qY2s"
}
```

# 根据分享链接打开文件

**还没实现**

`/api/link/+20位的随机字符串`

### 需要参数

无

### 返回结果

跟read_file一样

