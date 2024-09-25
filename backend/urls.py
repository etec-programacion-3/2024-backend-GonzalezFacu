from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-auth/', include("rest_framework.urls")),
    path('api/', include("api.urls")),  # Asegúrate de que esta línea incluya la app que contiene las rutas para el registro
]