from os import name
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post", views.create, name="post"),
    path("edit/<int:id>", views.update, name="update_post"),
    path("profile/<int:id>", views.profile, name="profile"),
    path("like", views.like_unlike, name="like_unlike"),
    path("following", views.following, name="following"),
    path("follow/<int:id>", views.follow, name="follow"),
    path("unfollow/<int:id>", views.unfollow, name="unfollow")
]
