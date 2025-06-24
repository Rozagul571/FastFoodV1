from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager

class User(AbstractUser):
    class RoleType(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        WAITER = 'waiter', 'Waiter'
        USER = 'user', 'User'

    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    role = models.CharField(max_length=20, choices=RoleType.choices, default=RoleType.USER)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email']

    # username fieldni butunlay olib tashlash (bu muhim!)
    username = None

    objects = CustomUserManager()

    def __str__(self):
        return self.phone_number