from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import json
from django.views.decorators.csrf import csrf_exempt

from .models import Followers, User, Posts, Likes


def index(request) -> HttpResponse:
    posts = Posts.objects.all().order_by("-created_at")
    if request.user.is_authenticated:
        for post in posts:
            post.liked_by_user = post.likes.filter(user=request.user).exists()  # Corrected `like` to `likes`

    posts = Paginator(posts, 10)
    page_number = request.GET.get("page", 1)
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
            return redirect(reverse("index"))
            
    elif request.method == "GET":
        return redirect(reverse("index"))
 
 
@login_required
@csrf_exempt   
def update(request, id):
    if request.method == "POST":
        post = Posts.objects.get(pk=int(id))
        if post.user == request.user:
            data = json.loads(request.body)
            form = PostForm(data, instance=post)
            if form.is_valid():
                form.save()
                return JsonResponse({"message":"successfully editted the message"}, status = 302)
        elif request.method == "GET":
            return JsonResponse({"message":"successfully editted the message"}, status = 400)   
    
def profile(request, id):
    try:
        user = User.objects.prefetch_related("posts", "followers").get(id=id)
    except User.DoesNotExist:
        return redirect(reverse("index"))

    posts = Paginator(user.posts.all().order_by("-created_at"), 10)
    if request.user.is_authenticated:
        for post in posts.object_list:
            post.liked_by_user = post.likes.filter(user=request.user).exists()

    posts_page_number = request.GET.get("posts_page_number", 1)
    posts = posts.get_page(posts_page_number)
    follower_queryset =user.followers.all().order_by("follower__username")
    no_of_followers = follower_queryset.count()
    followers = Paginator(follower_queryset, 10)
    followers_page_number = request.GET.get("followers_page_number", 1)
    followers = followers.get_page(followers_page_number)

    follows = user.followers.filter(follower=request.user).exists()

    context = {
        "user_profile": user,
        "posts": posts,
        "followers": followers,
        "follows": follows,
        "no_of_followers": no_of_followers,
        "form": PostForm()
    }

    return render(request, "network/profile.html", context)


@login_required
def like_unlike(request):
    if request.method == "GET":
        post_id = request.GET.get("id")
        action = request.GET.get("action")
        
        if post_id is None or action not in ["like", "unlike"]:
            return JsonResponse({"error": "Invalid post ID or action."}, status=400)

        try:
            post = Posts.objects.get(pk=int(post_id))
        except Posts.DoesNotExist:
            return JsonResponse({"error": "Post not found."}, status=404)

        if action == "like":
            if not Likes.objects.filter(user=request.user, post=post).exists():
                Likes.objects.create(user=request.user, post=post)
                post.like_count += 1
                post.save()
        elif action == "unlike":
            if Likes.objects.filter(user=request.user, post=post).exists():
                Likes.objects.filter(user=request.user, post=post).delete()
                post.like_count -= 1
                post.save()

        return JsonResponse({"like_count": post.like_count}, status=200)
    return JsonResponse({"error": "Invalid request method."}, status=405)


@login_required
def following(request):
    if request.method == "GET":
        following = Followers.objects.filter(follower = request.user).values_list("user",flat=True)
        posts = Posts.objects.filter(user__in = following)
        for post in posts:
            post.liked_by_user = post.likes.filter(user=request.user).exists()
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
    Followers.objects.create(user=user, follower= follower)
    return redirect(reverse("profile", args = [id]))

@login_required
def unfollow(request, id):
    user = User.objects.get(pk=id)
    follower = request.user
    item = Followers.objects.filter(user=user, follower= follower)
    item.delete()
    return redirect(reverse("profile", args = [id]))
