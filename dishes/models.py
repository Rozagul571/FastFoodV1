from django.db import models
from restaurants.models import Restaurant

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='categories')
    parent_category = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subcategories')
    def __str__(self):
        return self.name

class Dish(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="dishes")
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    restaurant = models.ForeignKey('restaurants.Restaurant', on_delete=models.CASCADE, related_name='dishes')

    def __str__(self):
        return self.name