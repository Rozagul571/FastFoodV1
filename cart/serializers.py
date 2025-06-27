from rest_framework import serializers
from cart.models import Cart
from dishes.models import Dish
from restaurants.models import Restaurant

class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ('name', 'price')

class CartSerializer(serializers.ModelSerializer):
    dish_id = serializers.PrimaryKeyRelatedField(queryset=Dish.objects.all(), source='dish', write_only=True)
    restaurant_id = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all(), source='dish.restaurant', write_only=True)
    dish = DishSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = ('cart_id', 'user', 'dish_id', 'restaurant_id', 'quantity', 'dish', 'created_at', 'updated_at')
        read_only_fields = ('cart_id', 'user', 'created_at', 'updated_at', 'dish')

    def validate(self, data):
        dish = data['dish']
        restaurant_id = data.get('dish.restaurant')
        if restaurant_id and dish.restaurant_id != restaurant_id.id:
            raise serializers.ValidationError("Dish does not belong to the selected restaurant.")
        if data['quantity'] < 1:
            raise serializers.ValidationError("Quantity must be at least 1.")
        return data

    def create(self, validated_data):
        validated_data.pop('restaurant_id', None)
        cart_id = self.context['request'].session.get('cart_id')
        if not cart_id:
            cart = Cart.objects.create(**validated_data)
            self.context['request'].session['cart_id'] = str(cart.cart_id)
        else:
            cart = Cart.objects.filter(cart_id=cart_id, dish=validated_data['dish']).first()
            if cart:
                cart.quantity += validated_data['quantity']
                cart.save()
            else:
                cart = Cart.objects.create(**validated_data)
                self.context['request'].session['cart_id'] = str(cart.cart_id)
        return cart

    def update(self, instance, validated_data):
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()
        return instance