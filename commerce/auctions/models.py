from django.contrib.auth.models import AbstractUser
from django.db import models


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
    image_url = models.URLField(blank=True, null=True)
    category = models.ForeignKey(Category, blank=True)
    creator = models.ForeignKey(User, default=None)
    date = models.DateTimeField(default=datetime.now, blank=True)
    buyer = models.ForeignKey(User, default=None)
    current_bid = models.ForeignKey(Bid, related_name="Current_Price")
    watchlist = models.ManyToManyField(user, blank=True, related_name="Watchers")

class Bid(models.Model):
    item = models.ForeignKey(List, related_name="Item_bidded")
    bid = models.FloatField()
    user = models.ForeignKey(User, related_name="Buyer")
    date = models.DateTimeField(default=datetime.now, blank=True)

class Comment(models.Model):
    item = models.ForeignKey(List, related_name="Commented_item")
    comment = models.TextField()
    user = models.ForeignKey(User, related_name="Commentator")
    date = models.DateTimeField(default=datetime.now, blank=True)
