from django.contrib.auth.models import User
from django.db import models

from advertisements.models import City


class Profile(models.Model):

    user = models.OneToOneField(User, null=True)

    city = models.ForeignKey(City, null=True, blank=True)
