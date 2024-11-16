from django.contrib import admin
from .models import User, Followers, Posts, Likes
# Register your models here.

admin.site.register(User)
admin.site.register(Followers)
admin.site.register(Posts)
admin.site.register(Likes)