from rest_framework import viewsets, generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from users.serializers import UserSerializer, RegisterSerializer, WaiterCreateSerializer
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


class WaiterCreateView(APIView):
    permission_classes = [IsAuthenticated, Permissions]

    def post(self, request):
        # if request.user.role != 'admin':
        #     return Response({"error": "only admin can add waiters"}, status=status.HTTP_403_FORBIDDEN)

        serializer = WaiterCreateSerializer(data=request.data)
        if serializer.is_valid():
            waiter = serializer.save()
            return Response({"message": f"Waiter {waiter.phone_number} successfully added"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)