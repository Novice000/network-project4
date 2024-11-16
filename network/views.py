from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import Followers, User, Posts, Likes


def index(request) -> HttpResponse:
    posts = Posts.objects.all()
    posts = Paginator(posts,10)
    page_number = request.GET.get("page",1)
    posts = posts.get_page(page_number)
    return render(request, "network/index.html", {
        "posts": posts,
        "form": PostForm()
    })


def login_view(request) -> HttpResponseRedirect | HttpResponse:
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request) -> HttpResponseRedirect:
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request) -> HttpResponse | HttpResponseRedirect:
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

# @login_required
# def posts(request) -> HttpResponse:
#     posts = Posts.objects.all()
#     return render("network/index.html", {
#         "posts": posts
#     })

@login_required   
def create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit = False)
            post.user = request.user
            post.save()
            
    elif request.method == "GET":
        return redirect(reverse("index"))
    
def update(request, id):
    if request.method == "POST":
        post = Posts.objects.get(pk=int(id))
        if post.user == request.user:
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                form.save()
        elif request.method == "GET":
            return redirect(reverse("index"))   
    
def profile(request):
    if not request.method == "GET":
        return redirect(reverse("index"))
    
    id  = request.GET.get("id", None)
    
    if id is None:
        return redirect(reverse("index"))
    try:
        user = User.objects.prefetch_related("posts","followers").get(id = id)
    except User.DoesNotExist:
        return redirect(reverse("index"))
    
    posts = Paginator(user.posts.all().order_by("-created_at"),10)
    posts_page_number = request.GET.get("posts_page_number",1)
    posts = posts.get_page(posts_page_number)
    followers = Paginator(user.followers.all(), 10)
    followers_page_number = request.GET.get("followers_page_number",1)
    followers = followers.get_page(followers_page_number)
    
    follows = Followers.objects.filter(user= User.objects.get(pk=id), follower = request.user).exists()
    
    context = {
        "user": user,
        "posts": posts,
        "followers": followers,
        "follows": follows
    }
    
    return render(request, "network/profile.html", context)

def like_unlike(request):
    post_id = request.GET.get("id", None)
    action = request.GET.get("action", None)
    
    if post_id == None or action == None:
        return JsonResponse({
            "error": "Post id not found or Invalid action"
        }, 404)
        
    else:
        post = Posts.object.get(pk=int(id))
        post.like += 1
        likes = Likes.objects.create(user = post.user, fan = request.user)
        post.save()
        likes.save()
        return JsonResponse({
            "like_count": post.likes,
            "already_liked": True
        })

@login_required
def following(request):
    if request.method == "GET":
        following = Followers.objects.filter(follower = request.user).values_list("user",flat=True)
        posts = Posts.objects.filter(user__in = following)
        posts = Paginator(posts, 10)
        posts_page_number = request.GET.get("page",1)
        posts = posts.get_page(posts_page_number)
        form = PostForm()
        return render(request, "network/index.html", {
            "posts":posts,
            "form":form
        })
    else:
        return redirect(reverse("following"))
    
@login_required
def follow(request, id):
    user = User.objects.get(pk=id)
    follower = request.user
    Followers.object.create(user=user, follower= follower)
    return redirect(reverse("profile", args = [id]))

@login_required
def unfollow(request, id):
    user = User.objects.get(pk=id)
    follower = request.user
    item = Followers.object.filter(user=user, follower= follower)
    item.delete()
    return redirect(reverse("profile", args = [id]))
