# views.py
from rest_framework import generics, viewsets, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RegisterSerializer, CustomTokenObtainPairSerializer, ProductSerializer, ReviewSerializer, CartSerializer
from .models import Product, Review, Cart

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

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]  # Solo usuarios autenticados pueden acceder

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)  # Filtrar por usuario autenticado

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Asignar el usuario al carrito
