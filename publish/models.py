# publish/models.py
from django.db import models


class Author(models.Model):
    # Author表项，含用户名和密码，均为字符串属性，并设置最大长度
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=20)
