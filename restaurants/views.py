from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from restaurants.models import Restaurant
from restaurants.serializers import RestaurantSerializer, RestaurantCreateSerializer, WaiterSerializer
from fastfood.permissions import Permissions
from users.models import User


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.prefetch_related('waiters').all()
    # permission_classes = [Permissions]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return RestaurantCreateSerializer
        return RestaurantSerializer

    @action(detail=True, methods=['post'], permission_classes=[Permissions])
    def add_waiter(self, request, pk=None):
        restaurant = self.get_object()
        serializer = WaiterSerializer(data=request.data)
        if serializer.is_valid():
            waiter = User.objects.get(id=serializer.validated_data['id'])
            restaurant.waiters.add(waiter)
            return Response({'status': 'Waiter added'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[Permissions])
    def remove_waiter(self, request, pk=None):
        restaurant = self.get_object()
        serializer = WaiterSerializer(data=request.data)
        if serializer.is_valid():
            waiter = User.objects.get(id=serializer.validated_data['id'])
            restaurant.waiters.remove(waiter)
            return Response({'status': 'Waiter deleted'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)