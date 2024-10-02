# views.py
from rest_framework import generics, viewsets, permissions
from .serializers import RegisterSerializer, CustomTokenObtainPairSerializer, ProductoSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Producto


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = []  # Permitir acceso sin autenticación

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [permissions.AllowAny]
