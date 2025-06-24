from django.urls import path
from orders.views import OrderListCreateView

urlpatterns = [
    path('', OrderListCreateView.as_view(), name='orders'),
]