from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import CustomUser, Product, Review

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password']

    def create(self, validated_data):
        user = CustomUser(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Añade atributos personalizados al token aquí si es necesario

        return token

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if not user:
                raise ValidationError('Invalid email or password')

            attrs['user'] = user
            return super().validate(attrs)
        
        raise ValidationError('Please provide both email and password')

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'rating', 'name', 'description', 'price', 'stock', 'image', 'categories']

class ReviewSerializer(serializers.ModelSerializer):
    product = ProductSerializer()  # Cambiar a 'product' (minúscula)

    class Meta:
        model = Review
        fields = ['id', 'product', 'author', 'rating', 'content', 'created_at']
    
    def create(self, validated_data):
        review = Review(**validated_data)
        review.save()  # Esto llamará al método save que actualiza el rating del producto
        return review