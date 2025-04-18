# models.py
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models


from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("El email es obligatorio")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    image = models.ImageField(upload_to='users/', default='users/placeholderUserImage.jpg')
    country_code = models.CharField(max_length=5, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    street = models.CharField(max_length=100, blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email



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
