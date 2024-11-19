from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Followers(models.Model):
    class Meta:
        verbose_name = "Follower"
        verbose_name_plural = "Followers"
        unique_together = ('user', 'follower')
        
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    
    def __str__(self) -> str:
        return f"{self.follower.username} follows {self.user.username}"


class Posts(models.Model):
    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    post_title = models.CharField(max_length=30)
    post = models.CharField(max_length=400)
    like_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    
    def __str__(self) -> str:
        return f"'{self.post_title}' by {self.user.username} on {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"


class Likes(models.Model):
    class Meta:
        verbose_name = "Like"
        verbose_name_plural = "Likes"
        unique_together = ('user', 'post')
        
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liked_posts")
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name="likes")  # Changed related_name to "likes"
    
    def __str__(self) -> str:
        return f"{self.user.username} likes '{self.post.post_title}'"
