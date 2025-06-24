# users/serializers.py
from rest_framework import serializers
from users.models import User

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