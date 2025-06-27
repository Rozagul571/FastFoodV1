# from django_filters import rest_framework as filters
# from orders.models import Order
#
#
# class OrderFilter(filters.FilterSet):
#     restaurant = filters.CharFilter(field_name='restaurant', lookup_expr='exact')
#     dish = filters.CharFilter(field_name='dish', lookup_expr='exact')
#     status = filters.CharFilter(choices = Order.Status.choices, field_name='status')
#     class Meta:
#         fields = ('restaurant', 'dish')
