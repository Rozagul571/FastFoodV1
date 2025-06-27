from django_filters import rest_framework as filters
from dishes.models import Category, Dish


class CategoryFilter(filters.FilterSet):
    class Meta:
        model = Category
        fields = ('name', 'description')

class DishFilter(filters.FilterSet):
    class Meta:
        model = Dish
        fields = ('name', 'description')

