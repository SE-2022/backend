# saving/models.py
from django.db import models


class Article(models.Model):
    # Author表项，含用户名和密码，均为字符串属性，并设置最大长度
    name = models.CharField(max_length=100, primary_key=True)
    raw = models.CharField(max_length=65535, null=True)
