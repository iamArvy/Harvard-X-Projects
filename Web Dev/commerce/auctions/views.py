from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from . import models
from django.contrib.auth.decorators import login_required
from .forms import CreateListingForm, CommentForm
from django.contrib import messages
from .models import User

# Listing

def listing(request, listing_id):
    # """View for a single listing."""
    # Get the current user (if logged in) and their listings
    user = request.user
    cform = CommentForm()
    content = get_object_or_404(models.Listings, pk=listing_id)
    comments = models.Comments.objects.filter(clist=content)
    messages_data = messages.get_messages(request)
    messages_list = [str(message) for message in messages_data]
    if request.user.is_authenticated:
        user_bid = models.Bids.objects.filter(user=request.user, list=content)
    else:
        user_bid = None
    bidders = models.Bids.objects.filter(list=content).count()
    if bidders == 0:
        highest_bid = None
    else:
        highest_bid = models.Bids.objects.filter(list=content).order_by('amount')[0]
    return render(request, "auctions/listing.html", {
        'content': content,
        'user': user,
        'messages': messages_list,
        'user_bid': user_bid,
        'bidders': bidders,
        'highest_bid': highest_bid,
        'cform': cform,
        'comments': comments
    })

def category(request, category_id):
        content = get_object_or_404(models.Categories, pk=category_id)
        listing = models.Listings.objects.filter(cat=content)
        return render(request, 'auctions/categories.html',{
            'listings':listing,
            'cate':content
        })

def close(request, listing_id):
    user = request.user
    content = get_object_or_404(models.Listings, pk=listing_id)
    if content.user == user:
        content.is_active = False
        content.save()
    else:
        messages.error(request, "You are not Authorized to perform this actions")
    return redirect('listing', listing_id=listing_id)

@login_required
def bid(request, id):
    amount = request.POST['bid']
    user = request.user
    listing = get_object_or_404(models.Listings, pk=id)
    if int(amount) <= int(listing.startprice):
        messages.error(request, "Bid must be more than Starting Price")
    if listing.highestbid and int(amount) <= int(listing.highestbid.amount):
        messages.error(request, "Bid must be more than Highest Bid")
    else:
        bidlist, created = models.Bids.objects.get_or_create(user=user, list=listing)
        bidlist.amount = int(amount)
        bidlist.save()
        listing.highestbid = bidlist
        listing.save()
        if not user.watchlist.filter(pk=listing.pk).exists():
            user.watchlist.add(listing)
            user.save()
        messages.success(request, 'Your Bid is Successful')

    return redirect('listing', listing_id=id)

@login_required
def add_to_watchlist(request, id):
    # id = request.POST['id']
    listing = get_object_or_404(models.Listings, pk=id)
    user = request.user
    user.watchlist.add(listing)
    user.save()
    return redirect('listing', listing_id=id)

@login_required
def delete_from_watchlist(request, id):
    # id = request.POST['id']
    listing = get_object_or_404(models.Listings, pk=id)
    user = request.user
    user.watchlist.remove(listing)
    user.save()
    return redirect('listing', listing_id=id)

@login_required
def add_comment(request, listing_id):
    user = request.user
    listing = get_object_or_404(models.Listings, pk=listing_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        newComment = form.save(commit=False)
        newComment.user = user
        newComment.clist = listing
        newComment.save()
        return redirect("listing", listing_id=listing_id)
#Auths
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
def watchlist(request):
    try:
        user = request.user
        user_watchlist = user.watchlist
        listings = user_watchlist.all()
    except user.watchlist.all == None:
        listings = None

    return render(request, "auctions/watchlist.html", {"listings": listings})

#index
def index(request):
    listings = models.Listings.objects.filter(is_active=True)
    categories = models.Categories.objects.all()
    return render(request, "auctions/index.html",{
        'listings': listings,
        'categories': categories
    })

@login_required
def create(request):
    user = request.user
    if request.method == "POST":
        form = CreateListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.user = request.user
            listing.save()
            user.auctions.add(listing)
            user.save
            return redirect("listing", listing_id=listing.id)
    else:
        form = CreateListingForm()

    return render(request, "auctions/create.html", {"form": form})


@login_required
def auctions(request):
    try:
        user = request.user
        user_watchlist = user.auctions
        listings = user_watchlist.all()
    except user.watchlist.all == None:
        listings = None
    return render(request, "auctions/auctions.html", {"listings": listings})
