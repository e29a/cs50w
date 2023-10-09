from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    content = models.CharField(max_length=500)
    author = models.CharField(max_length=64)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField()
    class Meta:
        ordering = ['-timestamp']

class Follow(models.Model):
    follower = models.CharField(max_length=64)
    following = models.CharField(max_length=64)

class Like(models.Model):
    post = models.IntegerField()
    user = models.IntegerField()