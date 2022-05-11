from django.db import models


# from file.models import File


class User(models.Model):
    userID = models.AutoField(primary_key=True, editable=False)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=20)
    avatar = models.ImageField(upload_to='avatar')
    email = models.CharField(max_length=50)
    root_file = models.ForeignKey(
        'file.File',
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='yy'
    )

    def to_dict(self):
        return {
            'username': str(self.username),
            'password': str(self.password),
            'email': str(self.email),
        }
