
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,)
    forget_password_token=models.CharField(max_length=400)
    date_created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

from django.db import models

class Tweetsdata(models.Model):
    user_tags = models.CharField(max_length=255)
    timestamp = models.DateTimeField()
    tweet = models.TextField()
    reply = models.TextField()
    retweets =  models.CharField(max_length=255)
    likes =  models.CharField(max_length=255)
