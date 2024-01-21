from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Place(models.Model):
    google_api_place_id = models.CharField(null=False, primary_key=True, max_length=256)
    name = models.CharField(null=False, max_length=256)
    rating = models.CharField(null=False, max_length=256)
    open_now = models.CharField(null=True, max_length=256)
    mobile_number = models.CharField(null=True, max_length=256)
    location = models.CharField(null=False, max_length=256)
    photos = models.TextField(null=True)
    reviews = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Place: {self.name}, ID: {self.google_api_place_id}"

    def to_dict(self):
        return {
            'google_api_place_id': self.google_api_place_id,
            'name': self.name,
            'rating': self.rating,
            'open_now': self.open_now,
            'mobile_number': self.mobile_number,
            'location': self.location,
            'photos': self.photos,
            'reviews': self.reviews,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

"""Use inbuilt Django model that comes with User Authentication"""
# class User(models.Model):
#     username = models.CharField(null=False, max_length=256)
#     password = models.CharField(null=False, max_length=256)
#     email = models.CharField(null=True, max_length=256)
#     verification_link = models.CharField(null=True, max_length=256)
#     email_verified = models.BooleanField(null=False, default=False)

class Bookmark(models.Model):
    # id = models.IntegerField(null=False, primary_key=True)
    user_id = models.CharField(null=False, max_length=256)
    user_name = models.CharField(null=False, max_length=256)
    place_id = models.ForeignKey(Place, on_delete=models.CASCADE)
    bookmarked = models.BooleanField(default=False, null=False)

    def __str__(self):
        return f"Bookmark: {self.user_name} - {self.place_id.name}"

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'user_name': self.user_name,
            'place_id': self.place_id.google_api_place_id,
            'bookmarked': self.bookmarked
        }

