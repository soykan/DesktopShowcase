from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    email = models.CharField(max_length=255, unique=True)

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.CharField(max_length=1000)
    photo = models.ImageField()
    point = models.IntegerField(default=0)

class LikesAndUsers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

