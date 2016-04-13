from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class City(models.Model):

    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Category(models.Model):
    """
    A broad category of advertisements. It's view displays all of the items
    within it's subcategories.
    """
    title = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.title


class SubCategory(models.Model):
    """
    Very similar to Category.
    """
    title = models.CharField(max_length=255, null=True)
    category = models.ForeignKey(Category, null=True)

    def __str__(self):
        return self.title


class Advertisement(models.Model):
    """
    The main object of the site. Ads are filtered by user, category, or
    subcategory and are displayed in a number of ways.
    """
    title = models.CharField(max_length=255, null=True)
    description = models.TextField(max_length=2000, null=True)
    price = models.IntegerField(null=True, blank=True)
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    image = models.ImageField(upload_to="advertisement_images/", null=True,
                              blank=True)
    email = models.EmailField(max_length=254, null=True)
    zipcode = models.CharField(max_length=10, null=True, blank=True)

    city = models.ForeignKey(City, null=True)
    subcategory = models.ForeignKey(SubCategory, null=True)
    user = models.ForeignKey(User, null=True, blank=True)

    created_time = models.DateTimeField(auto_now_add=True, null=True)
    modified_time = models.DateTimeField(auto_now=True, null=True)

    @property
    def display_date(self):
        date = self.modified_time
        return "{:%b} {}".format(date, date.day)

    def __str__(self):
        return self.title
