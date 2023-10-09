from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import *


def index(request):
    
    posts = Post.objects.all()
    paginator = Paginator(posts, 10)
    page_num = request.GET.get('page', 1)

    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request, "network/index.html", {
        "posts": page_obj
    })


def login_view(request):
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


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
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

def new(request):
    content = request.POST['content']
    author = request.user.username
    new_post = Post(content=content, author=author, likes=0)
    new_post.save()
    return HttpResponseRedirect('/')

def profile(request, user):
    user = User.objects.get(username=user)
    posts = Post.objects.filter(author = request.user.username)
    followers = Follow.objects.filter(following = request.user.username).count()
    following = Follow.objects.filter(follower = request.user.username).count()

    return render(request, "network/profile.html", {
        "user" : user,
        "posts" : posts,
        "followers" : followers,
        "following" : following
    }) 

def edit(request, id):
    post = Post.objects.get(id=id)
    if request.method == "GET":
        return render(request, "network/edit.html", {
            "post": post
        })
    else:
        content = request.POST["content"]
        post.content = content
        post.save()
        return HttpResponseRedirect("/")

def following(request):
    results = []
    followings = Follow.objects.filter(follower = request.user.username)
    posts = Follow.objects.all()

    for post in posts:
        for following in followings:
            if post.author == following.following:
                results.append[post]
            else:
                pass
    
    paginator = Paginator(results, 8)
    page_num = request.GET.get('page', 1)

    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request, "network/following.html", {
        "posts": page_obj
    })

def follow(request, user):
    follow = Follow(follower=request.user.username, following=user)
    follow.save()
    return HttpResponseRedirect("/")

def unfollow(request, user):
    unfollow = Follow.objects.get(follower=request.user.username, following=user)
    unfollow.delete()
    return HttpResponseRedirect("/")

@login_required
def like(request, id):
    post = Post.objects.get(id=id)
    post_likes = Like.objects.filter(post=post.id)
    check = []

    if post_likes:
        for post_like in post_likes:
            if post_like.user == request.user.id:
                check.append(post_like)
                break

    if not check:
        post.likes = post.likes + 1
        post.save()
        like = Like(user=request.user.id, post=id)
        like.save()
    else:
        post.likes = post.likes - 1
        post.save()
        like = Like.objects.get(user=request.user.id, post=id)
        like.delete()
    
    return JsonResponse(post.serialize())


                
    


