from rest_framework import serializers
from restaurants.models import Restaurant
from django.contrib.gis.geos import Point

# class WaiterSerializer(serializers.Serializer):
    # waiter_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='waiter'), source='id')

    # def validate_waiter_id(self, value):
    #     if not value.role == 'waiter':
    #         raise serializers.ValidationError("Foydalanuvchi waiter roli bo‘lishi kerak.")
    #     return value

class RestaurantCreateSerializer(serializers.ModelSerializer):
    latitude = serializers.FloatField(write_only=True)
    longitude = serializers.FloatField(write_only=True)
    location = serializers.HiddenField(default=None)

    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'latitude', 'longitude', 'location')
        read_only_fields = ('id', 'location')

    def validate(self, data):
        latitude = data['latitude']
        longitude = data['longitude']
        data['location'] = Point(longitude, latitude)
        return data

    def create(self, validated_data):
        validated_data.pop('latitude', None)
        validated_data.pop('longitude', None)
        return Restaurant.objects.create(**validated_data)

class RestaurantSerializer(serializers.ModelSerializer):
    latitude = serializers.FloatField(source='location.y', read_only=True)
    longitude = serializers.FloatField(source='location.x', read_only=True)

    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'latitude', 'longitude')
        read_only_fields = ('id', 'latitude', 'longitude')