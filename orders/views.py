from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from orders.models import Order
from orders.serializers import OrderSerializer
from rest_framework.permissions import IsAuthenticated

class OrderListCreateView(ListCreateAPIView):
    queryset = Order.objects.select_related('user', 'restaurant').prefetch_related('order_items').order_by('created_at')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return self.queryset
        return self.queryset.filter(user=user)

class OrderRetrieveUpdateView(RetrieveUpdateAPIView):
    queryset = Order.objects.select_related('user', 'restaurant').prefetch_related('order_items').order_by('created_at')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return self.queryset
        return self.queryset.filter(user=user)