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

