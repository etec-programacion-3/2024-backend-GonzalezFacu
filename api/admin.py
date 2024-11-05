# djsr/authentication/admin.py
from django.contrib import admin
from .models import CustomUser,  Product, Category, Review, Difficulty, Cart, CartItem
class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Difficulty)
admin.site.register(Review)
admin.site.register(Cart)
admin.site.register(CartItem)
