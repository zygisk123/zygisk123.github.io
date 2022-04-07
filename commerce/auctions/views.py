from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib import messages

from .models import User, Category, List, Bid, Comment

class ItemForm(ModelForm):
    class Meta:
        model = List
        fields = ['title', 'description', 'starting_price', 'category', 'image_url']

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['bid']

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

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
        messages.success(request, '"Item is created"')
        return HttpResponseRedirect(reverse("index"))
#        return render(request, "auctions/index.html", {
#            "message": "Item is created"
#        })
    else:
        return render(request, "auctions/new_item.html", {
            "form": ItemForm()
        })    

# I get all data from models.py List model and display information in item_entry.html
def item_page(request, item_id):
    item = List.objects.get(pk=item_id)
    comments = Comment.objects.filter(item=item_id).order_by('date')
    commentform= CommentForm()
    if request.user.is_authenticated:
        if item.offers == True:
            highest_bid = Bid.objects.filter(item=item_id).order_by('bid').first()
            if item.active == True:
                return render(request, "auctions/item_entry.html", {
                "item": item,
                "bid_form": BidForm(),
                "bidder": highest_bid.user,
                "bid": item.current_bid,
                "commentform": commentform,
                "comments": comments,
            })
            else:
                return render(request, "auctions/item_closed.html", {
                "item": item,
            })
        else:
            return render(request, "auctions/item_entry.html", {
                "item": item,
                "bid_form": BidForm(),
                "commentform": commentform,
                "comments": comments
            })
    else:
        return render(request, "auctions/item_entry.html", {
            "item": item,
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
        highest_bid = Bid.objects.filter(item=item_id).order_by('bid').first()
        messages.success(request, 'Item is deleted from your watchlist')
        return HttpResponseRedirect(reverse("item_page", args=(item.id,)))
    else:
    # 5. if item not in users list. Item is added
        item.watchlist.add(request.user)
        item.added = True
        item.save()
        highest_bid = Bid.objects.filter(item=item_id).order_by('bid').first()
        messages.success(request, 'Item added to your watchlist')
        return HttpResponseRedirect(reverse("item_page", args=(item.id,)))
   #             return render(request, "auctions/item_entry.html", {
    #        "message": "Item added to your watchlist",
     #       "item": item,
      #      "bid_form": BidForm(),
       #     "bidder": highest_bid.user,
        #    "message": "Item added to your watchlist"
         #})


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

@login_required
def bid(request, item_id):
    # POST method
    if request.method=="POST":
        # create form (BidForm=Bid from models.py)
        form = BidForm(request.POST)
        # check if form is valid
        if form.is_valid():
            # get posted info
            bid = float(form.cleaned_data["bid"])
            # make sure that auction exist
            try:
                item = List.objects.get(pk=item_id)
            except List.DoesNotExist:
                highest_bid = Bid.objects.filter(item=item_id).order_by('bid').first()
                messages.success(request, "Auction doesn't exist")
                return HttpResponseRedirect(reverse("item_page", args=(item.id,)))
#                   "item": item,
 #                   "message": "Auction doesn't exist",
  #                  "bid_form": BidForm(),
   #                 "bidder": highest_bid.user 
    #            })
            # getting starting price for item
            starting_price = item.starting_price
            # gettting current bid of the same item
            current_bid = float(item.current_bid)
            # getting user which made bid
            user = request.user
            # checking whether item has atleast one offer or no
            if item.offers == False:
                # if item has no offers bid must be equal or bigger to starting price
                if bid < starting_price:
                    highest_bid = Bid.objects.filter(item=item_id).order_by('bid').first()
                    messages.success(request, "Your bid is too low.")
                    return HttpResponseRedirect(reverse("item_page", args=(item.id,)))
 #                   return render(request, "auctions/item_entry.html", {
  #                      "message": "Your bid is too low.",
   #                    "bid_form": BidForm(),
    #                    "bidder": highest_bid.user 
     #               })
            else:
                # if item has atleast one offer bid must be bigger than current price
                if bid <= current_bid:
                    highest_bid = Bid.objects.filter(item=item_id).order_by('bid').first()
                    messages.success(request, "Your bid is too low.")
                    return HttpResponseRedirect(reverse("item_page", args=(item.id,)))
 #                   return render(request, "auctions/item_entry.html", {
  #                      "message": "Your bid is too low.",
   #                     "item": item,
    #                    "bid_form": BidForm(),
     #                   "bidder": highest_bid.user 
      #              })
            # checking whether bidder is items creator
            if item.creator == user:
                highest_bid = Bid.objects.filter(item=item_id).order_by('bid').first()
                messages.success(request, "Item's creator cannot bid")
                return HttpResponseRedirect(reverse("item_page", args=(item.id,)))
 #               return render(request, "auctions/item_entry.html", {
  #                  "message": "Item's creator cannot bid",
   #                 "item": item,
    #                "bid_form": BidForm(),
     #               "bidder": highest_bid.user 
      #          })
            # if all checks are correct than we can save data to List model for tam tikram item
            # this means that item has atleast one offer
            item.offers = True
            # changing current price to biggest bid
            item.current_bid = bid
            # data is saved
            item.save()
            add_bid = Bid(item = item, bid = bid, user = user)
            add_bid.save()
            highest_bid = Bid.objects.filter(item=item_id).order_by('bid').first()
            messages.success(request, "Your bid is accepted!")
            return HttpResponseRedirect(reverse("item_page", args=(item.id,)))
#            return render(request, "auctions/item_entry.html", {
 #               "message": "Your bid is accepted!",
  #              "item": item,
   #             "bid_form": BidForm(),
    #            "bidder": highest_bid.user 
     #       })
    else:
        item = List.objects.get(pk=item_id)
        bid = item.current_bid
        highest_bid = Bid.objects.filter(item=item_id).order_by('bid').first()
        return HttpResponseRedirect(reverse("item_page", args=(item.id,)))
#        return render(request, "auctions/item_entry.html", {
 #           "item": item,
  #          "bid": bid,
   #         "bid_form": BidForm(),
    #        "bidder": highest_bid.user 
     #   })

def endbid(request, item_id):
    # find particular item
    item = List.objects.get(pk=item_id)
    # find info about winner from Bid model
    winner = Bid.objects.filter(item=item_id).order_by('bid').first()
    # makes the listing no longer active
    item.active = False
    # add ausctions winner to the List model
    item.buyer == winner.user
    item.save()
    # date when user won auction
    date = datetime.now() 
    return render (request, "auctions/end_auction.html", {
        "date": date,
        "winner": winner
    })

@login_required
def comment(request, item_id):
    if request.method=="POST":
        item = List.objects.get(pk=item_id)
        commentform = CommentForm(request.POST)
        if commentform.is_valid():
            form = commentform.save(commit=False)
            form.comment = commentform.cleaned_data["comment"]
            form.user = request.user
            form.item = item
            form.save()
            return HttpResponseRedirect(reverse("item_page", args=(item.id,)))
        messages.success(request, "Please fill comment form")
        return HttpResponseRedirect(reverse("item_page", args=(item.id,)))
    else:
        return HttpResponseRedirect(reverse("item_page", args=(item.id,)))

def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories,
    })

def item_list(request, category_id):
    category = Category.objects.get(pk=category_id)
    items = List.objects.filter(active=True, category=category).order_by("title")
    if len(items) == 0:
        messages.success(request, "There is no items in this category")
        return render(request, "auctions/items_list.html")

    return render(request, "auctions/items_list.html",{
        "items": items
    })












