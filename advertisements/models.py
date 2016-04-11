from django.contrib.auth.models import User
from django.db import models


class City(models.Model):

    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Category(models.Model):

    title = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.title


class SubCategory(models.Model):

    title = models.CharField(max_length=255, null=True)
    category = models.ForeignKey(Category, null=True)

    def __str__(self):
        return self.title


class Advertisement(models.Model):

    title = models.CharField(max_length=255, null=True)
    description = models.TextField(max_length=2000, null=True)
    price = models.IntegerField(null=True, blank=True)
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    image = models.ImageField(upload_to="advertisement_images/", null=True, blank=True)
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
