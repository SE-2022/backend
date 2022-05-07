# saving (unused now)/models.py
import datetime

from django.db import models


class Article(models.Model):
    # Author表项，含用户名和密码，均为字符串属性，并设置最大长度
    name = models.CharField(max_length=100, primary_key=True)
    createTime = models.DateTimeField(
        # default="2000-01-01",
        auto_now_add=True)
    lastEditTime = models.DateTimeField(
        # default="2000-01-01",
        auto_now=True)
    raw = models.CharField(max_length=65535, null=True)
