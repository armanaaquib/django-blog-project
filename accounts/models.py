from django.db import models
from django.contrib import auth

# Create your models here.
class UserProfile(auth.models.User):
    portfolio_site = models.URLField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def __str__(self):
        return f'@{self.username}'
