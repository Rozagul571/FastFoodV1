import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import UUIDField
from restaurants.models import Restaurant
from users.managers import CustomUserManager
class User(AbstractUser):
    class RoleType(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        WAITER = 'waiter', 'Waiter'
        USER = 'user', 'User'
    # id = UUIDField(default=uuid.uuid4, editable=False, unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    role = models.CharField(max_length=20, choices=RoleType.choices, default=RoleType.USER)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email']

    username = None
    objects = CustomUserManager()

    def __str__(self):
        return self.phone_number

class Waiter(User):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='waiters')
    def save(self, *args, **kwargs):
        self.role = self.RoleType.WAITER
        super().save(*args, **kwargs)