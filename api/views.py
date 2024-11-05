# views.py
from rest_framework import generics, viewsets, permissions
from .serializers import RegisterSerializer, CustomTokenObtainPairSerializer, ProductSerializer, ReviewSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Product, Review

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = []  # Permitir acceso sin autenticación

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        review = serializer.save()  # Guardar la reseña
        product = review.product  # Obtener el producto relacionado
        product.update_rating()  # Actualizar el rating del producto