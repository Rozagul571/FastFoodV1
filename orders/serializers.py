from rest_framework import serializers
from orders.models import Order, OrderItem
from dishes.models import Dish
from restaurants.models import Restaurant
from django.contrib.gis.geos import Point
from orders.utils import calculate_totals, estimate_delivery, calculate_distance
from decimal import Decimal

class OrderItemSerializer(serializers.ModelSerializer):
    dish_id = serializers.PrimaryKeyRelatedField(queryset=Dish.objects.all(), source='dish', write_only=True)
    dish = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'dish', 'dish_id', 'quantity', 'price')
        read_only_fields = ('id', 'price')

    # def validate(self, data):
    #     dish = data['dish']
    #     quantity = data['quantity']
    #     if quantity < 1:
    #         raise serializers.ValidationError("Quantity kamida 1 bo‘lishi kerak.")
    #     if not dish.is_available:
    #         raise serializers.ValidationError(f"{dish.name} taomi mavjud emas.")
    #     return data

    def create(self, validated_data):
        dish = validated_data['dish']
        validated_data['price'] = dish.price
        return super().create(validated_data)

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    restaurant_id = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all(), source='restaurant', write_only=True)
    latitude = serializers.FloatField(write_only=True)
    longitude = serializers.FloatField(write_only=True)
    location = serializers.HiddenField(default=None)
    distance_km = serializers.FloatField(read_only=True, allow_null=True)
    delivery_fee = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True, allow_null=False, default=0.00)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    estimated_time = serializers.IntegerField(read_only=True)
    delivery_address = serializers.CharField(read_only=True)

    class Meta:
        model = Order
        fields = (
            'id', 'user', 'restaurant_id', 'status', 'delivery_address', 'location',
            'latitude', 'longitude', 'distance_km', 'delivery_fee', 'total_price',
            'estimated_time', 'order_items', 'created_at', 'updated_at'
        )
        read_only_fields = (
            'id', 'user', 'status', 'delivery_address', 'location', 'distance_km',
            'delivery_fee', 'total_price', 'estimated_time', 'created_at', 'updated_at'
        )

    def validate(self, data):
        restaurant = data['restaurant']
        latitude = data['latitude']
        longitude = data['longitude']
        order_items = data['order_items']

        # if not -90 <= latitude <= 90:
        #     raise serializers.ValidationError("Kenglik -90 va 90 oralig‘ida bo‘lishi kerak.")
        # if not -180 <= longitude <= 180:
        #     raise serializers.ValidationError("Uzunlik -180 va 180 oralig‘ida bo‘lishi kerak.")
        #
        # if not restaurant.location:
        #     raise serializers.ValidationError(f"{restaurant.name} restoranining lokatsiyasi o‘rnatilmagan.")
        #
        # for item in order_items:
        #     dish = item['dish']
        #     if dish.restaurant != restaurant:
        #         raise serializers.ValidationError(f"{dish.name} taomi {restaurant.name} restoraniga tegishli emas.")

        data['location'] = Point(longitude, latitude)
        data['delivery_address'] = f"latitude: {latitude}, longitude: {longitude}"

        return data

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')
        restaurant = validated_data['restaurant']
        user = self.context['request'].user
        location = validated_data['location']
        delivery_address = validated_data['delivery_address']

        distance_km = calculate_distance(location, restaurant.location)
        order = Order.objects.create(
            user=user,
            restaurant=restaurant,
            delivery_address=delivery_address,
            location=location,
            distance_km=distance_km
        )

        order_items = [
            OrderItem(
                order=order,
                dish=item_data['dish'],
                quantity=item_data['quantity'],
                price=item_data['dish'].price
            )
            for item_data in order_items_data
        ]
        OrderItem.objects.bulk_create(order_items)

        total_time = estimate_delivery(order)
        quantity, items_price, total, delivery_fee = calculate_totals(order)

        order.estimated_time = total_time
        order.total_price = total
        order.delivery_fee = delivery_fee
        order.save()

        return order

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        user = self.context['request'].user
        if user.role not in ['admin', 'restaurant']:
            return {
                'id': rep['id'],
                'restaurant_id': rep['restaurant_id'],
                'delivery_address': rep['delivery_address'],
                'total_price': rep['total_price'],
                'estimated_time': rep['estimated_time'],
                'order_items': rep['order_items'],
                'created_at': rep['created_at']
            }
        return rep