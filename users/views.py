from rest_framework import viewsets, generics, permissions
from users.models import User
from users.serializers import UserSerializer, RegisterSerializer
from fastfood.permissions import Permissions

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [Permissions]

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.role == 'admin':
            return self.queryset
        if self.request.user.is_authenticated:
            return self.queryset.filter(id=self.request.user.id)
        return self.queryset.none()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]