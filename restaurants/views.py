from rest_framework import viewsets
from restaurants.models import Restaurant
from restaurants.serializers import RestaurantSerializer, RestaurantCreateSerializer


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    # permission_classes = [Permissions]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return RestaurantCreateSerializer
        return RestaurantSerializer
