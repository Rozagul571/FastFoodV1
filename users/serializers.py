from rest_framework import serializers
from restaurants.models import Restaurant
from users.models import User, Waiter


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone_number', 'email', 'first_name', 'last_name', 'role')
        read_only_fields = ('role',)

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('phone_number', 'email', 'first_name', 'last_name', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            phone_number=validated_data['phone_number'],
            email=validated_data.get('email'),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            password=validated_data['password'],
            role=User.RoleType.USER
        )
        return user


class WaiterCreateSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=15)
    first_name = serializers.CharField(max_length=255, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=255, required=False, allow_blank=True)
    restaurant_id = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all(), source='restaurant')

    class Meta:
        model = Waiter
        fields = ('phone_number', 'first_name', 'last_name', 'restaurant_id')

    def create(self, validated_data):
        restaurant = validated_data.pop('restaurant')
        user = User.objects.create_user(
            phone_number=validated_data['phone_number'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=User.RoleType.WAITER
        )
        waiter = Waiter.objects.get(user_id=user.user_id)
        waiter.restaurant = restaurant
        waiter.save()
        return waiter