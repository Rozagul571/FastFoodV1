from django.db import models
from django.contrib.gis.db.models import PointField
from users.models import User

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    location = PointField()
    waiters = models.ManyToManyField(User, related_name='restaurants', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name