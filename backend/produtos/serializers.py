from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Product, Cart

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = '__all__'
    


class ProductSerializer(serializers.ModelSerializer):
    product_image = serializers.ImageField(use_url=True)
    class Meta:
        model = Product
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = Cart
        fields = '__all__'