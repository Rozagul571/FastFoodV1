from django.urls import path
from cart.views import CartView

urlpatterns = [
    path('', CartView.as_view(), name='cart-list'),
    # path('<int:dish_id>/', CartUpdateDeleteView.as_view(), name='cart-update-delete'),
]