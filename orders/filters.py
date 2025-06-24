from django_filters import rest_framework as filters
from orders.models import Order

class OrderFilter(filters.FilterSet):
    restaurant = filters.NumberFilter(field_name='restaurant__id')
    status = filters.ChoiceFilter(choices=Order.Status.choices)

    class Meta:
        model = Order
        fields = ['restaurant', 'status']