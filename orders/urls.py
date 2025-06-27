from django.urls import path
from orders.views import OrderListCreateView, OrderRetrieveUpdateView

urlpatterns = [
    path('', OrderListCreateView.as_view(), name='order-list'),
    path('<int:pk>/', OrderRetrieveUpdateView.as_view(), name='order-detail'),
]