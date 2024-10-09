# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # No es necesario requerir username

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)  # Nombre de la categoría
    descripcion = models.TextField(blank=True, null=True)  # Descripción opcional

    def __str__(self):
        return self.nombre
    
class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    imagen = models.ImageField(upload_to='productos/')
    categorias = models.ManyToManyField(Categoria, related_name='productos')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
    
    from django.db import models

class Review(models.Model):
    product = models.ForeignKey('Producto', on_delete=models.CASCADE)  # Relación con el producto
    user_name = models.CharField(max_length=100)  # Nombre del usuario que deja la reseña
    rating = models.DecimalField(max_digits=2, decimal_places=1)  # Puntuación, por ejemplo, de 1 a 5
    content = models.TextField()  # Contenido de la reseña
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha de creación


