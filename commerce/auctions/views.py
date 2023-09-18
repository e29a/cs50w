from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import *


def index(request):
    listings = Listing.objects.filter(listing_status="open")
    closed = Listing.objects.filter(listing_status="closed")
    return render(request, "auctions/index.html", {
        "listings": listings,
        "closed": closed
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create(request):
    if request.method == "GET":
        return render(request, "auctions/create.html")
    else:
        title = request.POST["title"]
        description = request.POST["description"]
        price = request.POST["price"]
        image = request.POST["image"]
        category = request.POST["category"]
        
        if request.user.is_authenticated:
            new_listing = Listing(listing_title=title, listing_author_id=request.user.id, listing_description=description, listing_price=price, listing_image=image, listing_category=category, listing_status="open")
            new_listing.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            new_listing = Listing(listing_title=title, listing_author_id="anonymous", listing_description=description, listing_price=price, listing_image=image, listing_category=category)
            return HttpResponseRedirect(reverse('index'))

def listing(request, id):
    listing = Listing.objects.get(id=id)
    comments = Comment.objects.filter(comment_listing_id=id)

    check = Watchlist.objects.filter(listing_id=id)

    if len(check) == 0:
        iswatchlist = "no"
    else:
        iswatchlist = "yes"

    return render(request, "auctions/listing.html", {
        "listing" : listing,
        "comments" : comments,
        "iswatchlist": iswatchlist
    })

@login_required
def watchlist(request):
    watchlist = Watchlist.objects.filter(user_id=request.user.id)
    return render(request, "auctions/watchlist.html", {
        "watchlist" : watchlist
    })

@login_required
def addWatchlist(request, id):
    listing_id = Listing.objects.get(id=id).id
    listing_title = Listing.objects.get(id=id).listing_title
    user_id = request.user.id
    new_item = Watchlist(listing_title=listing_title, listing_id=listing_id, user_id=user_id)
    new_item.save()
    messages.success(request, 'The listing has been added to watchlist successfully.')
    return HttpResponseRedirect("/")

def rmWatchlist(request, id):
    listing = Watchlist.objects.get(listing_id=id)
    listing.delete()
    messages.success(request, 'Removed item from watchlist successfully')
    return HttpResponseRedirect("/")

def categories(request):
    categories = Listing.objects.values('listing_category').distinct()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })


def category(request, c):
    items = Listing.objects.filter(listing_category=c)
    return render(request, "auctions/category.html", {
        "items": items,
        "category": c
    })

@login_required
def bid(request, id):
    bid = request.GET["amount"]
    listing = Listing.objects.get(id=id)
    if int(bid) <= listing.listing_price:
        messages.error(request, 'Bid must be higher than current price')
        return HttpResponseRedirect("/")
    else:
        listing.listing_price = bid
        listing.listing_winner = request.user.username
        listing.save()
        messages.success(request, 'The bid has been created successfully.')
        return HttpResponseRedirect("/listing/{}".format(id))

@login_required
def comment(request, id):
    content = request.GET["content"]
    comment = Comment(comment_listing_id=id, comment_user_id=request.user.username, comment_content=content)
    comment.save()
    messages.success(request, 'The comment has been created successfully.')
    return HttpResponseRedirect("/listing/{}".format(id))

def close(request, id):
    listing = Listing.objects.get(id=id)
    listing.listing_status = "closed"
    listing.save()
    messages.success(request, 'The listing has been closed successfully.')
    return HttpResponseRedirect("/")