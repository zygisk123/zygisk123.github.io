from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime

class User(AbstractUser):
    pass

class Category(models.Model):
    category = models.CharField(unique=True, max_length=30)
    
    def __str__(self):
        return f"{self.category}"

class List(models.Model):
    title = models.CharField(max_length=20)
    description = models.TextField()
    starting_price = models.FloatField()
    image_url = models.URLField(blank=True, null=True, max_length=2000)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="Category")
    creator = models.ForeignKey(User, on_delete=models.PROTECT, related_name="Creators_listing")
    date = models.DateTimeField(default=datetime.now)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="Buyer")
    current_bid = models.FloatField( default=0.00)
    watchlist = models.ManyToManyField(User, blank=True, default="", related_name="watchers")
    added = models.BooleanField(default=False) #added to watchlist or not
    offers = models.BooleanField(default=False) #has offers or no

    def __str__(self):
        return f"Title: {self.title} Starting price: {self.starting_price} Current bid: {self.current_bid}"

class Bid(models.Model):
    item = models.ForeignKey(List, on_delete=models.CASCADE, related_name="Item_bidded")
    bid = models.DecimalField(max_digits=20, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return f"{self.item} Bid: {self.bid} Buyer {self.user}"

class Comment(models.Model):
    item = models.ForeignKey(List, on_delete=models.CASCADE, related_name="Commented_item")
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Commentator")
    date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return f"{self.item} comment: {self.comment} user: {self.user} date:{self.date}"
