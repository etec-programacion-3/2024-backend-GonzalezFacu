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
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.DecimalField(max_digits=1, decimal_places=0, default=0)
    stock = models.IntegerField()
    image = models.ImageField(upload_to='products/')
    categories = models.ManyToManyField(Category, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Review(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)  # Relation with the product
    user_name = models.CharField(max_length=100)  # Name of the user leaving the review
    rating = models.DecimalField(max_digits=2, decimal_places=1)  # Rating, e.g., from 1 to 5
    content = models.TextField()  # Content of the review
    created_at = models.DateTimeField(auto_now_add=True)  # Creation date
