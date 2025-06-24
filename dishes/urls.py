from django.urls import path, include
from rest_framework.routers import DefaultRouter
from dishes.views import DishViewSet, CategoryViewSet

router = DefaultRouter()
router.register('', DishViewSet, basename='dish')
router.register('categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
]