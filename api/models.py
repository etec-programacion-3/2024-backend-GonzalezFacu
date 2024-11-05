# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # Not necessary to require username

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Category name
    description = models.TextField(blank=True, null=True)  # Optional description

    def __str__(self):
        return self.name
    
class Difficulty(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    shortDescription = models.CharField(max_length=255, default="")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0)  # Cambia el max_digits a 2 para permitir decimales
    stock = models.IntegerField()
    prepTime = models.IntegerField(default=0)
    difficulty = models.ManyToManyField(Difficulty, related_name='products')
    image = models.ImageField(upload_to='products/')
    categories = models.ManyToManyField(Category, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def update_rating(self):
        reviews = self.review_set.all()  # Obtener todas las reseñas relacionadas
        if reviews.exists():
            average_rating = reviews.aggregate(models.Avg('rating'))['rating__avg']
            self.rating = round(average_rating, 1)  # Redondear a 1 decimal
            self.save()  # Guardar el producto con el nuevo rating
    
class Review(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)  # Relación con el producto
    author = models.CharField(max_length=100)  # Nombre del autor de la reseña
    rating = models.DecimalField(max_digits=2, decimal_places=1)  # Rating, por ejemplo, de 1 a 5
    content = models.TextField()  # Contenido de la reseña
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha de creación

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Llamar al método save original
        self.product.update_rating()  # Actualizar el rating del producto relacionado

class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)  # Relación con el usuario
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Cart of {self.user.email}'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)  # Relación con el carrito
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Relación con el producto
    quantity = models.PositiveIntegerField(default=1)  # Cantidad del producto

    def __str__(self):
        return f'{self.quantity} of {self.product.name} in {self.cart.user.email} cart'

    class Meta:
        unique_together = ('cart', 'product')  # Evitar duplicados en el carrito
