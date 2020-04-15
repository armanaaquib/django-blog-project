from django.db import models
from django.contrib import auth

# Create your models here.
class UserProfile(auth.models.User):
    portfolio_site = models.URLField(blank=True)
    profile_pic = models.ImageField(blank=True)

    def __str__(self):
        return f'@{self.username}'
