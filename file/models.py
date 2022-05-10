from django.db import models

from team.models import Team
from user.models import User


# class Directory(models.Model):
#     dir_name = models.CharField(max_length=100)
#     dirID = models.AutoField(primary_key=True, editable=False, null=False)
#     create_time = models.DateTimeField(auto_now_add=True)
#     file_num = models.IntegerField(default=0)
#     userID = models.ForeignKey(User, on_delete=models.CASCADE, to_field='userID')
#
#     class Meta:
#         db_table = 'Directory'
#
#     def __unicode__(self):
#         return 'dir_name:%s|file_num:%s' % (self.dir_name, self.file_num)


class File(models.Model):
    FileID = models.AutoField(primary_key=True, editable=False, null=False)
    isDir = models.BooleanField(null=False, default=False)
    username = models.CharField(max_length=100)
    file_name = models.CharField(max_length=100)
    create_time = models.DateTimeField(auto_now_add=True)
    last_modify_time = models.DateTimeField(auto_now=True)
    userID = models.ForeignKey(User, on_delete=models.CASCADE, to_field='userID')
    TeamID = models.ForeignKey(Team, to_field='teamID', on_delete=models.CASCADE)
    # dirID = models.ForeignKey(Directory, to_field='dirID', on_delete=models.CASCADE)
    fatherId = models.IntegerField(default=0)
    commentFul = models.BooleanField(default=True)
    content = models.TextField()
    isDelete = models.BooleanField(default=False)  # If the file has been deleted, this value is True.

    class Meta:
        db_table = 'File'

    def __unicode__(self):
        return 'file_name:%s' % self.file_name


class Comment(models.Model):
    CommentID = models.AutoField(primary_key=True, editable=False)
    comment_time = models.DateTimeField(auto_now_add=True)
    comment_fileID = models.ForeignKey(File, to_field='FileID', on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, to_field='userID', on_delete=models.CASCADE)
