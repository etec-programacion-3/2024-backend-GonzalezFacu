from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileView, RegisterView, CustomTokenObtainPairView, ProductViewSet, ReviewViewSet, CartViewSet
from . import views

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'cart', CartViewSet, basename='cart')

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', RegisterView.as_view(), name='register'),
    path('api/products/<int:product_id>/', views.get_product_by_id, name='get_product_by_id'),
    path('review/', ReviewViewSet.as_view({'get': 'list'}), name='review'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('', include(router.urls)),
]
