from django.db import models

from user.models import User


class Message(models.Model):
    msg_userID = models.ForeignKey(User, to_field='userID', on_delete=models.CASCADE)
    msg_send_time = models.DateTimeField(auto_now_add=True)
    msg_contend = models.TextField()
    msg_isRead = models.BooleanField(default=False)
