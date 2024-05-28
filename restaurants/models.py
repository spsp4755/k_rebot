from django.db import models
from django.contrib.auth.models import User

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    service = models.CharField(max_length=255, blank=True, null=True)
    menu1 = models.CharField(max_length=255, blank=True, null=True)
    menu2 = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

class SavedRestaurant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} saved {self.restaurant.name}"
