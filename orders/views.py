from rest_framework.generics import ListCreateAPIView
from orders.models import Order
from orders.serializers import OrderSerializer
from fastfood.permissions import Permissions
from django_filters.rest_framework import DjangoFilterBackend
from orders.filters import OrderFilter

class OrderListCreateView(ListCreateAPIView):
    queryset = Order.objects.select_related('user', 'restaurant').prefetch_related('order_items').all()
    serializer_class = OrderSerializer
    permission_classes = [Permissions]
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter