from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    listing_title = models.CharField(max_length=64)
    listing_author_id = models.IntegerField()
    listing_description = models.CharField(max_length=150)
    listing_price = models.IntegerField()
    listing_image = models.CharField(max_length=64)
    listing_category = models.CharField(max_length=64)
    listing_status = models.CharField(max_length=64)
    listing_winner = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.id}: {self.listing_title}"

class Bid(models.Model):
    bid_listing_id = models.IntegerField()
    bid_user_id = models.IntegerField()
    bid_amount = models.IntegerField()

class Comment(models.Model):
    comment_listing_id = models.IntegerField()
    comment_user_id = models.CharField(max_length=64)
    comment_content = models.CharField(max_length=64)

class Watchlist(models.Model):
    listing_id = models.IntegerField()
    listing_title = models.CharField(max_length=64)
    user_id = models.IntegerField()

    