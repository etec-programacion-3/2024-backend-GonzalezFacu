# urls.py
from django.urls import path
from .views import RegisterView, CustomTokenObtainPairView, ProductoViewSet


urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', RegisterView.as_view(), name='register'),
    path('productos/', ProductoViewSet.as_view({'get': 'list'}), name='producto'),
    # otras rutas...
]
