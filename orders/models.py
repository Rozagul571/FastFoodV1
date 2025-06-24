
from django.db import models
from django.contrib.gis.db import models as gis_models
from users.models import User
from restaurants.models import Restaurant
from dishes.models import Dish

class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        ACCEPTED = 'accepted', 'Accepted'
        PREPARING = 'preparing', 'Preparing'
        DELIVERING = 'delivering', 'Delivering'
        DELIVERED = 'delivered', 'Delivered'
        CANCELLED = 'cancelled', 'Cancelled'

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='orders')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=Status.choices,
                              default=Status.PENDING)
    delivery_address = models.CharField(max_length=255)
    location = gis_models.PointField()
    distance_km = models.FloatField(null=True, blank=True)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True,
                                       blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    estimated_time = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.dish.name}"


