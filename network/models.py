from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Followers(models.Model):
    class Meta:
        verbose_name = "Follower"
        verbose_name_plural = "Followers"
        
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "followers")
    follower = models.ForeignKey(User, on_delete = models.CASCADE, related_name="following")
    
    def __str__(self) -> str:
        return f"{self.user} follows {self.follower}"
    
class Likes(models.Model):
    class Meta:
        verbose_name = "Like"
        verbose_name_plural = "Likes"
        
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "likes")
    fan = models.ForeignKey(User, on_delete = models.CASCADE, related_name="liker")

class Posts(models.Model):
    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        
    user = models.ForeignKey(User, on_delete= models.CASCADE, related_name="posts")
    post_title = models.CharField(max_length=30)
    post = models.CharField(max_length = 400)
    likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f"{self.user} posted {self.post_title} on {self.created_at}"
    