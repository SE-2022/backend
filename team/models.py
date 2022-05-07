from django.db import models


from user.models import User


class Team(models.Model):
    teamID = models.AutoField(primary_key=True, editable=False)
    team_name = models.CharField(max_length=50)
    team_avatar = models.ImageField(upload_to='team_avatar')
    managerID = models.ForeignKey(User, to_field='userID', on_delete=models.CASCADE)
