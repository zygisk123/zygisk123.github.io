from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm
from django.contrib.auth.decorators import login_required

from .models import User, Category, List, Bid, Comment

class ItemForm(ModelForm):
    class Meta:
        model = List
        fields = ['title', 'description', 'starting_price', 'category', 'image_url']


def index(request):
    return render(request, "auctions/index.html", {
        "items": List.objects.all()
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

# Creating function that let user to create new item
# 1. Importing form (created from model List)
# 2. Checking if posted data is valid
# 3. Save submitted form to memory not data base using: commit:False
# 4. Made changes to the data. Added creator to the form to achieve that I used request.user
# 5. saved form and when form is submitted user is redirected to the index.html page
# 6. @login_required show that user must be signed up to the page  
@login_required
def NewItem(request):
    if request.method == "POST":
        itemform = ItemForm(request.POST)
        if itemform.is_valid():
            form = itemform.save(commit=False)
            form.creator = request.user
            form.save()
        return render(request, "auctions/index.html", {
            "message": "Item is created"
        })
    else:
        return render(request, "auctions/new_item.html", {
            "form": ItemForm()
        })    

# I get all data from models.py List model and display information in item_entry.html
def item_page(request, item_id):
    item = List.objects.get(pk=item_id)
    return render(request, "auctions/item_entry.html", {
        "item": item
    })



 
@login_required
def watchlist(request, item_id):
    # 1. Accessing item
    item = List.objects.get(pk=item_id)

    # 2. get all watchers for that one item
    watchers = item.watchlist.all()
    # 3. get signed up user
    user = request.user

    # 4. check if this user already has this item in his list
    # if this is true item will be deleted
    if user in watchers:
        item.watchlist.remove(request.user)
        item.added = False
        item.save()
        return render(request, "auctions/item_entry.html", {
        "message": f"Item was deleted from your watchlist" ,
        "item": item,
    })
    else:
    # 5. if item not in users list. Item is added
        item.watchlist.add(request.user)
        item.added = True
        item.save()
        return render(request, "auctions/item_entry.html", {
            "message": f"Item added to your watchlist",
            "item": item,
        })

def mylist(request):
    items = List.objects.all()
    user = request.user
    user_list=[]
    for item in items:
        watchers = item.watchlist.all()
        for watcher in watchers:
            if user == watcher:
                user_list.insert(0, item)
    return render(request, "auctions/my_list.html", {
        "user_list": user_list
    })



