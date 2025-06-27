import uuid
from rest_framework import serializers
from cart.models import Cart
from dishes.models import Dish

class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ('name', 'price')

class CartSerializer(serializers.ModelSerializer):
    dish_id = serializers.IntegerField(write_only=True)
    restaurant_id = serializers.IntegerField(write_only=True)
    dish = DishSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = ('cart_id', 'user', 'dish_id', 'restaurant_id', 'quantity', 'dish', 'created_at', 'updated_at')
        read_only_fields = ('cart_id', 'user', 'created_at', 'updated_at', 'dish')

    def validate(self, data):
        dish_id = data.get('dish_id')
        restaurant_id = data.get('restaurant_id')
        quantity = data.get('quantity', 1)

        if not dish_id:
            raise serializers.ValidationError("dish_id is required.")
        try:
            dish = Dish.objects.get(id=dish_id)
        except Dish.DoesNotExist:
            raise serializers.ValidationError(f"Dish with id {dish_id} does not exist.")

        if restaurant_id and dish.restaurant_id != restaurant_id:
            raise serializers.ValidationError("Dish does not belong to the selected restaurant.")
        if quantity < 1:
            raise serializers.ValidationError("Quantity must be at least 1.")

        data['dish'] = dish
        return data

    def create(self, validated_data):
        validated_data.pop('dish_id', None)
        validated_data.pop('restaurant_id', None)
        cart_id = self.context['request'].session.get('cart_id') or str(uuid.uuid4())
        cart = Cart.objects.filter(cart_id=cart_id, dish=validated_data['dish']).first()
        if cart:
            cart.quantity += validated_data['quantity']
            cart.save()
        else:
            cart = Cart.objects.create(cart_id=cart_id, **validated_data)
        self.context['request'].session['cart_id'] = cart.cart_id
        return cart

    def update(self, instance, validated_data):
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()
        return instance