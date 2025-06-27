from rest_framework import serializers
from orders.models import Order, OrderItem
from dishes.models import Dish
from restaurants.models import Restaurant
from cart.models import Cart
from django.contrib.gis.geos import Point
from orders.utils import calculate_distance, calculate_totals, estimate_delivery
from decimal import Decimal

class OrderItemSerializer(serializers.ModelSerializer):
    dish_id = serializers.PrimaryKeyRelatedField(queryset=Dish.objects.all(), source="dish", write_only=True)
    dish = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'dish', 'dish_id', 'quantity', 'price')
        read_only_fields = ('id', 'price')

    def create(self, validated_data):
        dish = validated_data['dish']
        validated_data['price'] = dish.price
        return super().create(validated_data)

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    restaurant_id = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all(), source="restaurant", write_only=True)
    latitude = serializers.FloatField(write_only=True)
    longitude = serializers.FloatField(write_only=True)
    location = serializers.HiddenField(default=None)
    distance_km = serializers.FloatField(read_only=True, allow_null=True)
    delivery_fee = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True, allow_null=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    preparation_time = serializers.IntegerField(read_only=True)
    delivery_time = serializers.IntegerField(read_only=True)
    estimated_time = serializers.IntegerField(read_only=True)
    delivery_address = serializers.CharField(read_only=True)

    class Meta:
        model = Order
        fields = (
            'id', 'user', 'restaurant_id', 'status', 'delivery_address', 'location',
            'latitude', 'longitude', 'distance_km', 'delivery_fee', 'preparation_time', 'delivery_time', 'estimated_time',
            'order_items', 'total_price', 'created_at', 'updated_at'
        )
        read_only_fields = (
            'id', 'user', 'status', 'delivery_address', 'location', 'distance_km',
            'delivery_fee', 'preparation_time', 'delivery_time',
            'estimated_time', 'total_price', 'created_at', 'updated_at'
        )

    def validate(self, data):
        restaurant = data['restaurant']
        latitude = data['latitude']
        longitude = data['longitude']
        user = self.context['request'].user

        cart_items = Cart.objects.filter(user=user).select_related('dish')
        if not cart_items.exists():
            raise serializers.ValidationError({"error": "No active cart found for this user."})

        for item in cart_items:
            if item.dish.restaurant_id != restaurant.id:
                raise serializers.ValidationError(f"Dish with id {item.dish_id} does not belong to {restaurant.name}.")

        data['location'] = Point(latitude, longitude)
        data['delivery_address'] = f"latitude: {latitude}, longitude: {longitude}"
        return data

    def create(self, validated_data):
        order_items_data = []
        restaurant = validated_data['restaurant']
        user = self.context['request'].user
        location = validated_data['location']
        delivery_address = validated_data['delivery_address']

        cart_items = Cart.objects.filter(user=user).select_related('dish')

        distance_km = calculate_distance(location, restaurant.location)
        if distance_km is None:
            distance_km = None
            delivery_fee = None
        else:
            delivery_fee = Decimal(str(distance_km * 5000)).quantize(Decimal('0.01'))

        order = Order.objects.create(
            user=user,
            restaurant=restaurant,
            delivery_address=delivery_address,
            location=location,
            distance_km=distance_km,
            delivery_fee=delivery_fee
        )

        for item in cart_items:
            order_items_data.append(OrderItem(order=order, dish=item.dish, quantity=item.quantity, price=item.dish.price))

        OrderItem.objects.bulk_create(order_items_data)
        estimated_time = estimate_delivery(order)
        quantity, items_price, total, delivery_fee = calculate_totals(order)
        order.estimated_time = estimated_time
        order.total_price = total
        order.save()

        cart_items.delete()

        return order

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        user = self.context['request'].user
        if user.role != 'admin':
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