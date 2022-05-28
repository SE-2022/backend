## 文档管理接口

[toc]

### 错误码

| 错误码 | 错误类型                         |
| ------ |------------------------------|
| 2001   | 创建文档   文件名缺失                 |
| 2002   | 创建文档   文件名重复                 |
| 2003   | 删除文档   文件不存在                 |
| 2004   | 删除文档  文件已被删除                 |
| 2005   | 创建文件夹 文件夹名称缺失                |
| 2006   | 创建文件夹 文件夹名称重复                |
| 2007   | 删除文件夹   删除文件夹失败              |
| 2008   | 恢复文档   无法恢复                  |
| 2009   | 用户未登录                        |
| 2010   | 请求方式错误                       |
|2101| 试图访问团队文件，但用户不属于这个团队          |
|2103| 试图访问团队文件，但此文件正被其它用户使用        |
|2104| 试图关闭文件，但目前并未持有此文件            |
|2105| 试图对非团队文件做团队文件才支持的操作，比如修改访问权限 |
|2106| 普通成员试图修改团队文件权限|
|2107| 试图将权限修改为不合法的值|


#### 创建文档

- Path:/newfile

- Method:POST

- 前端request格式：

  ```json
  {
  	"username":"xxx",
    "userID":xxx ,
    "file_name":"xxx",
    "commentFul":(boolean)
  }
  ```

- 后端response格式：

  ```json
  //成功
  {
    "errno":0,
    "create_time": "xxxx-xx-xx-xx:xx",
    "last_modify_time":"xxxx-xx-xx-xx:xx",
    "commentFul":True, //文章是否可评论，该属性默认为true
    "msg":"新建成功"
  }
  ```

  - 异常处理

    - 文件名缺失

      ```json
      //文件名重复
      {
        "errno":2001,
        "msg":"文件名不能为空"
      }
      ```

    - 文件名重复

      ```json
      //文件名重复
      {
        "errno":2002,
        "msg":"文件名重复"
      }
      ```

#### 删除文档

注：执行删除文档操作后，文档被放入回收站，仍可恢复。若需彻底删除该文档，应在回收站种执行“彻底删除”操作

- Path:/deletefile

- Method:POST

- 前端request格式：

  ```json
  {  
    "username":"xxx",  
    "userID":xxx ,
    "file_name":"xxx",
    "FileID":xxx
  }
  ```

- 后端response格式：

  - 个人工作台文件列表返回格式：

  ```json
  //成功
  {
    "errno":0,
    "msg":"文档删除成功",
    "fileList": [
     {
    "file_Name": "xxxx",
    "create_time": "xxxxxx",
    "last_modift_time": "xxxxxx",
     },
     {
    "file_name": "xxxx",
    "create_time": "xxxxxx",
    "last_modify_time": "xxxxxx",
     },
     ...
   ]
  }
  ```

  - 回收站文件列表返回格式：

  ```json
  {
    "fileList": [
     {
    "file_Name": "xxxx",
    "create_time": "xxxxxx",
    "last_modift_time": "xxxxxx",
     },
     {
    "fileName": "xxxx",
    "createTime": "xxxxxx",
    "lastEditTime": "xxxxxx",
     },
     ...
   ]
  }
  ```

  - 异常处理

    - 文件不存在

      ```json
      //文件不存在
      {
        "errno":2003,
        "msg":"文件名不存在"
      }
      ```

    - 文件已被删除

      ```json
      {
        "errno":2004,
        "msg":"文件已被删除"
      }
      ```

      

#### 创建文件夹

- Path:/mkdir

- Method:POST

- 前端request格式：

  ```json
  {
  	"username":"xxx",
    "userID":xxx ,
    "dir_name":"xxx"
  }
  ```

- 后端response格式:

  - 个人工作台文档列表

  ```json
  //成功
  {
    "errno":0,
    "create_time": "xxxx-xx-xx-xx:xx",  //文件夹创建时间
    "msg":"新建文件夹成功",
    "fileList": [
     {
    "file_Name": "xxxx",
    "create_time": "xxxxxx",
    "last_modift_time": "xxxxxx"
     },
     {
    "file_name": "xxxx",
    "create_time": "xxxxxx",
    "last_modify_time": "xxxxxx"
     },
      //...
   ],
   "dirList": [
    {
      "dir_name":"xxx",
      "file_num":x
    },
    {
      "dir_name":"xxx",
      "file_num":x
    },
    //...
  ]
  }
  ```

  - 异常处理

    - 文件夹名称缺失

      ```json
      //文件不存在
      {
        "errno":2005,
        "msg":"文件夹名称不能为空"
      }
      ```

    - 文件夹名称重复

      ```json
      //文件夹与已有名称重复
      {
        "errno":2006,
        "msg":"文件夹名称重复"
      }
      ```

#### 删除文件夹

- Path:/deletedir

- Method:POST

- 前端request格式：

  ```json
  {
  	"username":"xxx",
    "userID":xxx ,
    "dir_name":"xxx",
    "dirID":xxx
  }
  ```

- 后端response格式:

  - 个人工作台文档列表：

  ```json
  //成功
  {
    "errno":0,
    "msg":"删除文件夹成功",
    "fileList": [
     {
    "file_Name": "xxxx",
    "create_time": "xxxxxx",
    "last_modift_time": "xxxxxx"
     },
     {
    "file_name": "xxxx",
    "create_time": "xxxxxx",
    "last_modify_time": "xxxxxx"
     },
      //...
   ],
   "dirList": [
    {
      "dir_name":"xxx",
      "file_num":x
    },
    {
      "dir_name":"xxx",
      "file_num":x
    },
    //...
  ]
  }
  ```

  - 异常处理

    - 

      ```json
      //文件不存在
      {
        "errno":2007,
        "msg":"删除文件夹失败"
      }
      ```

#### 查看文件夹内容

- Path:/cddir

- Method:POST

- 前端request格式：

  ```json
  {
  	"username":"xxx",
    "userID":xxx ,
    "dir_name":"xxx",
    "dirID":xxx
  }
  ```

- 后端response格式:

  - 文件夹内文档列表：

  ```json
  //成功
  {
    "errno":0,
    "fileList": [
     {
    "file_Name": "xxxx",
    "create_time": "xxxxxx",
    "last_modift_time": "xxxxxx"
     },
     {
    "file_name": "xxxx",
    "create_time": "xxxxxx",
    "last_modify_time": "xxxxxx"
     },
      //...
   ],
  }
  ```

#### 在文件夹中添加文档

- Path:/addfile

- Method:POST

- 前端request格式：

  ```json
  {
  	"username":"xxx",
    "userID":xxx ,
    "dir_name":"xxx",
    "dirID":xxx,
     "file_name": "xxxx",
    "FileID":xxx
  }
  ```

- 后端response格式:

  - 文件夹内文档列表：

  ```json
  //成功
  {
    "errno":0,
    "fileList": [
     {
    "file_Name": "xxxx",
    "create_time": "xxxxxx",
    "last_modift_time": "xxxxxx"
     },
     {
    "file_name": "xxxx",
    "create_time": "xxxxxx",
    "last_modify_time": "xxxxxx"
     },
      //...
   ],
  }
  ```

  - 个人工作台文档列表：

    ```json
    "fileList": [
       {
      "file_Name": "xxxx",
      "create_time": "xxxxxx",
      "last_modift_time": "xxxxxx"
       },
       {
      "file_name": "xxxx",
      "create_time": "xxxxxx",
      "last_modify_time": "xxxxxx"
       },
        //...
     ],
    ```

#### 彻底删除文档

注：文档被放入回收站后才可执行彻底删除操作，执行该操作后，文档不可恢复

- Path:/desertfile

- Method:POST

- 前端request格式：

  ```json
  {
    "username":"xxx",
    "userID":xxx ,
    "file_name":"xxx",
    "FileID":xxx
  }
  ```

- 后端response格式：

  - 回收站文档列表返回格式：

    ```json
    {
      "fileList": [
       {
      "file_Name": "xxxx",
      "create_time": "xxxxxx",
      "last_modift_time": "xxxxxx",
       },
       {
      "fileName": "xxxx",
      "createTime": "xxxxxx",
      "lastEditTime": "xxxxxx",
       },
       ...
     ]
    }
    ```

#### 恢复文档

注：文档放入回收站后可被恢复

- Path:/restorefile

- Method:POST

- 前端request格式：

  ```json
  {
  	"username":"xxx",
    "userID":xxx ,
    "file_name":"xxx",
    "FileID":xxx
  }
  ```

- 后端response格式：

  - 个工作台文档列表返回格式

    ```json
    //成功
    {
      "fileList": [
       {
      "file_Name": "xxxx",
      "create_time": "xxxxxx",
      "last_modift_time": "xxxxxx",
       },
       {
      "file_name": "xxxx",
      "create_time": "xxxxxx",
      "last_modify_time": "xxxxxx",
       },
       ...
     ]
    }
    ```

  - 回收站文档列表返回格式

    ```json
    //成功
    {
      "errno":0,
      "msg":"文档删除成功",
      "fileList": [
       {
      "file_Name": "xxxx",
      "create_time": "xxxxxx",
      "last_modift_time": "xxxxxx",
       },
       {
      "file_name": "xxxx",
      "create_time": "xxxxxx",
      "last_modify_time": "xxxxxx",
       },
       ...
     ]
    }
    ```

  - 异常处理

    - 

      ```json
      {
        "errno":2008,
        "msg":"无法恢复"
      }
      ```

	#### 其他错误

- 用户未登录

  ```json
  {
    "errno":2009,
    "msg":"用户未登录"
  }
  ```

- 请求方式错误

```json
{
  "errno":2010,
  "msg":"请求方式错误"
}
```

