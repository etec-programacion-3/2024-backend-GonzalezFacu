# urls.py
from django.urls import path
from .views import RegisterView, CustomTokenObtainPairView, ProductViewSet, ReviewViewSet


urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', RegisterView.as_view(), name='register'),
    path('products/', ProductViewSet.as_view({'get': 'list'}), name='product'),
    path('review/', ReviewViewSet.as_view({'get': 'list'}), name='product'),
    # otras rutas...
]
