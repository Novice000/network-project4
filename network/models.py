from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Followers(models.Model):
    class Meta:
        verbose_nam = "Follower"
        verbose_name_plural = "Followers"
        
    user = models.ForeignKeyField(User, on_delete = models.CASCADE, related_name = "follower")
    follower = models.ForeignKeyField(User, on_delete = models.CASCADE, related_name="following")
    
    def __str__(self) -> str:
        return f"{self.user} follows {self.follower}"

class Posts(models.Model):
    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        
    user = models.ForeignKeyField(User, on_delete= models.CASCADE, related_name="posts")
    post_title = models.CharField(max_length=30)
    post = models.CharFieldKey(max_length = 400)
    likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f"{self.user} posted {self.post_title} on {self.created_at}"
    