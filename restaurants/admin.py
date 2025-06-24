from django.contrib import admin
from restaurants.models import Restaurant

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    pass