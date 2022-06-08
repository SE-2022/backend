from django.db import models

# Create your models here.
from file.models import File
from user.models import User


class Tag(models.Model):
    tagID = models.AutoField(primary_key=True, editable=False, null=False)
    tag_name = models.CharField(max_length=50)
    user = models.ForeignKey(
        User,
        # to_field='userID',
        on_delete=models.CASCADE,
        null=True,
    )
    tag_color = models.CharField(max_length=30, default='255')
    tag_details = models.CharField(max_length=100, null=False, default='这是标签的简介，你可以修改它')
    tag_count = models.IntegerField(default=0)


class TagFile(models.Model):
    id = models.AutoField(primary_key=True, editable=False, null=False)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
