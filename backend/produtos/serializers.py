from rest_framework import serializers
from .models import Product, Cart

class ProductSerializer(serializers.ModelSerialzer):
    class Meta:
        model = Product
        fields = '__all__'

class CartSerializer(serializers.ModelSerialzer):
    class Meta:
        model = Cart
        fields = '__all__'