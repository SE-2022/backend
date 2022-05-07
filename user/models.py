from django.db import models


class User(models.Model):
    userID = models.AutoField(primary_key=True, editable=False)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=20)
    avatar = models.ImageField(upload_to='avatar')
    nickname = models.CharField(max_length=30)
