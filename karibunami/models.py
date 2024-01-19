from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Place(models.Model):
    google_api_place_id = models.CharField(null=False, primary_key=True, max_length=256)
    name = models.CharField(null=False, max_length=256)
    rating = models.CharField(null=False, max_length=256)
    open_now = models.CharField(null=True, max_length=256)
    mobile_number = models.CharField(null=False, max_length=256)
    location = models.CharField(null=False, max_length=256)
    photos = models.TextField(null=True)
    reviews = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now=True)

"""Use inbuilt Django model that comes with User Authentication"""
# class User(models.Model):
#     username = models.CharField(null=False, max_length=256)
#     password = models.CharField(null=False, max_length=256)
#     email = models.CharField(null=True, max_length=256)
#     verification_link = models.CharField(null=True, max_length=256)
#     email_verified = models.BooleanField(null=False, default=False)
class Bookmark(models.Model):
    id = models.IntegerField(null=False, primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    place_id = models.ForeignKey(Place, on_delete=models.CASCADE)
    bookmarked = models.BooleanField(default=False, null=False)

