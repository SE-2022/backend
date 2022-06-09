from django.db import models

from team.models import Team
from user.models import User


class File(models.Model):
    fileID = models.AutoField(primary_key=True, editable=False, null=False)
    isDir = models.BooleanField(null=False, default=False)
    username = models.CharField(max_length=100)
    file_name = models.CharField(max_length=100)
    create_time = models.DateTimeField(auto_now_add=True)
    last_modify_time = models.DateTimeField(auto_now=True)
    last_read_time = models.DateTimeField(auto_now_add=True)  # 上次访问时间，只在read_file的时候会更新
    user = models.ForeignKey(
        User,
        # to_field='userID',
        on_delete=models.CASCADE,
        null=True,
    )
    team = models.ForeignKey(
        Team,
        to_field='teamID',
        on_delete=models.CASCADE,
        blank=True, null=True
    )
    team_perm = models.IntegerField(default=0)
    # dirID = models.ForeignKey(Directory, to_field='dirID', on_delete=models.CASCADE)
    fatherID = models.IntegerField(default=0)
    commentFul = models.BooleanField(default=True)
    content = models.CharField(max_length=65535, null=True)
    isDelete = models.BooleanField(default=False)  # If the file has been deleted, this value is True.
    # 文件互斥访问
    # 当有人以可写权限打开此文件，其它用户就只能以只读权限打开
    # 只读和可写两种权限的区别，在后端看只是能不能保存修改
    using = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='using')
    is_fav = models.BooleanField(default=False)

    class Meta:
        db_table = 'File'

    def __unicode__(self):
        return 'file_name:%s' % self.file_name

    def to_dic(self):
        return {
            'file_name': self.file_name,
            'create_time': self.create_time,
            # 'last_modify_time'
            'isDir': self.isDir,
        }


class Comment(models.Model):
    commentID = models.AutoField(primary_key=True, editable=False)
    comment_time = models.DateTimeField(auto_now_add=True)
    comment_fileID = models.ForeignKey(File, to_field='fileID', on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, to_field='userID', on_delete=models.CASCADE)
    content = models.TextField()


# # 团队文件权限表
# class TeamFile_Perm(models.Model):
#     file = models.ForeignKey(
#         File,
#         on_delete=models.CASCADE,
#         # related_name='xx',
#         null=True,
#     )
#     # 0：所有人读写
#     # 1：管理员读写，其余人只读
#     perm = models.IntegerField(default=0)

class File_share_link(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    perm = models.IntegerField()
    link = models.CharField(max_length=20)
    create_time = models.TimeField(auto_now_add=True)


class FileModel(models.Model):
    m_id = models.AutoField(primary_key=True, editable=False)
    m_name = models.CharField(max_length=100, unique=True)
    m_content = models.CharField(max_length=65535, null=True)
