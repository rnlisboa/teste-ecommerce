from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Product, Cart
from rest_framework.validators import UniqueValidator

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model=User
        fields='__all__'



class ProductSerializer(serializers.ModelSerializer):
    product_image=serializers.ImageField(use_url=True)
    
    class Meta:
        model=Product
        fields='__all__'
    def get_image_url(self, obj):
        return obj.image_url()

class CartSerializer(serializers.ModelSerializer):


    class Meta:
        model=Cart
        fields='__all__'
