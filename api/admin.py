# djsr/authentication/admin.py
from django.contrib import admin
from .models import CustomUser,  Producto, Categoria
class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Producto)
admin.site.register(Categoria)
