from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from restaurants.models import Restaurant
from restaurants.serializers import RestaurantSerializer, RestaurantCreateSerializer


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return RestaurantCreateSerializer
        return RestaurantSerializer
