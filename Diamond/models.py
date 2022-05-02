import django.utils.timezone as timezone

from django.db import models


# Create your models here.


class User(models.Model):
    userID = models.AutoField(primary_key=True, editable=False)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=20)
    avatar = models.ImageField(upload_to='avatar')
    nickname = models.CharField(max_length=30)


class Team(models.Model):
    teamID = models.AutoField(primary_key=True, editable=False)
    team_name = models.CharField(max_length=50)
    team_avatar = models.ImageField(upload_to='team_avatar')
    managerID = models.ForeignKey(User, to_field='userID', on_delete=models.CASCADE)


class File(models.Model):
    FileID = models.AutoField(primary_key=True, editable=False, null=False)
    username = models.CharField(max_length=100)
    file_name = models.CharField(max_length=100)
    # create_time = models.DateTimeField(auto_now_add=True)   default=timezone.now(),auto_now_add=True
    create_time = models.DateTimeField(auto_now_add=True)
    last_modify_time = models.DateTimeField(auto_now=True)
    userID = models.ForeignKey(User, on_delete=models.CASCADE, to_field='userID')
    TeamID = models.ForeignKey(Team, to_field='teamID', on_delete=models.CASCADE)
    commentFul = models.BooleanField(default=True)
    content = models.TextField()


class Comment(models.Model):
    CommentID = models.AutoField(primary_key=True, editable=False)
    comment_time = models.DateTimeField(auto_now_add=True)
    comment_fileID = models.ForeignKey(File, to_field='FileID', on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, to_field='userID', on_delete=models.CASCADE)


class Message(models.Model):
    msg_userID = models.ForeignKey(User, to_field='userID', on_delete=models.CASCADE)
    msg_send_time = models.DateTimeField(auto_now_add=True)
    msg_contend = models.TextField()
    msg_isRead = models.BooleanField(default=False)
