from django.shortcuts import render, get_objects_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTPP_400_BAD_REQUEST
from .models import Product, Cart
from .serializers import ProductSerializer, CartSerializer
# Create your views here.


class ProductAPIView(APIView):
    def get(self, request, format=None):
        # Buscando produtos no banco de dados
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)

        return Response(serializer.data, status=HTTP_200_OK)


