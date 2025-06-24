from rest_framework import viewsets
from dishes.models import Dish, Category
from dishes.serializers import DishSerializer, CategorySerializer
from fastfood.permissions import Permissions

class DishViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.select_related('category', 'restaurant').all()
    serializer_class = DishSerializer
    permission_classes = [Permissions]

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.select_related('restaurant').all()
    serializer_class = CategorySerializer
    permission_classes = [Permissions]