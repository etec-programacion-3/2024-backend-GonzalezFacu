# views.py
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Product
from rest_framework import generics, viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (
    RegisterSerializer,
    CustomTokenObtainPairSerializer,
    ProductSerializer,
    ReviewSerializer,
    CartSerializer,
    CartItemSerializer,
    UserProfileSerializer
)
from .models import Product, Review, Cart, CartItem

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = []  # Permitir acceso sin autenticación

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]


def get_product_by_id(request, product_id):
    # Obtener el producto por ID o devolver un error 404 si no existe
    product = get_object_or_404(Product, id=product_id)
    
    # Definir la información que queremos devolver en la respuesta
    product_data = {
        'id': product.id,
        'name': product.name,
        'price': str(product.price),  # Convertimos el precio a string para evitar problemas de formato JSON
        'image': product.image.url if product.image else None,  # Verificar si tiene imagen y devolver la URL
        'description': product.description,
    }
    
    # Retornar la respuesta JSON con los datos del producto
    return JsonResponse(product_data)


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
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # Custom action to add a product to the cart
    @action(detail=False, methods=['post'], url_path='add')
    def add_to_cart(self, request):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user)

        try:
            product = Product.objects.get(id=product_id)
            cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not item_created:
                cart_item.quantity += quantity  # Increase quantity if item already in cart
            else:
                cart_item.quantity = quantity  # Set initial quantity
            cart_item.save()
            return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

    # Custom action to update quantity in the cart
    @action(detail=False, methods=['patch'], url_path='update')
    def update_cart(self, request):
        item_id = request.data.get('item_id')
        quantity = request.data.get('quantity')
        user = request.user

        try:
            cart_item = CartItem.objects.get(id=item_id, cart__user=user)
            cart_item.quantity = quantity
            cart_item.save()
            return Response(CartItemSerializer(cart_item).data, status=status.HTTP_200_OK)
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found in cart"}, status=status.HTTP_404_NOT_FOUND)

    # Custom action to remove a product from the cart
    @action(detail=False, methods=['delete'], url_path='remove')
    def remove_from_cart(self, request):
        item_id = request.data.get('item_id')
        user = request.user

        try:
            cart_item = CartItem.objects.get(id=item_id, cart__user=user)
            cart_item.delete()
            return Response({"success": "Item removed from cart"}, status=status.HTTP_200_OK)
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found in cart"}, status=status.HTTP_404_NOT_FOUND)
