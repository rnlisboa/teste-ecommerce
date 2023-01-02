from django.shortcuts import render, get_object_or_404, get_list_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT
from .models import Product, Cart
from .serializers import ProductSerializer, CartSerializer, UserSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth import logout
from django.core.serializers import serialize
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

# Create your views here.

# Cadastro e login de usuário


class UserViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request):
        user = UserSerializer(request.user).data
        return Response(user)

    @action(detail=False, methods=['post'])
    def register(self, *args, **kwargs):
        queryset = User.objects
        req = self.request.data

        first_name = req.get('firstname')
        username = req.get('username')
        email = req.get('email')
        password = req.get('password')

        if not (username and first_name and email and password):
            return Response(f'Preencha todos os campos.', status=HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(data=req)
        if serializer.is_valid():
            user = User(
                username=username,
                first_name=first_name,
                email=email,
                is_active=True,
                is_superuser=False
            )
            user.set_password(password)
            user.save()

            user_serializer = UserSerializer(user, many=True)
            return Response("Cadastrado com sucesso.", status=HTTP_201_CREATED)

        return Response({
            "message": "Houveram erros de validação",
            "errors": serializer.errors
        }, status=HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def login(self, *args, **kwargs):
        req = self.request.data

        username = req.get('username')
        password = req.get('password')

        if not (username and password):
            return Response('Preencha todos os campos.', status=HTTP_400_BAD_REQUEST)

        user = auth.authenticate(
            self.request, username=username, password=password)
        print(user)
        if user is not None:
            auth.login(self.request, user)

            return Response({"user": username}, status=HTTP_200_OK)
        else:
            return Response('Usuario ou senha inválido', status=HTTP_400_BAD_REQUEST)

    

class ProductViewSet(viewsets.ViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def list(self, request):
        products = UserSerializer(request.user).data
        return Response(products)

    @action(detail=False, methods=['post'])
    def register(self, *args, **kwargs):
        req = self.request.data

        product_image = req.get('product_image')
        product_description = req.get('product_description')
        product_price = req.get('product_price')
        product_quantity = req.get('product_quantity')

        if not (product_description and product_image and product_price and product_quantity):
            return Response('Todos os campos são importantes.', status=HTTP_400_BAD_REQUEST)

        try:
            new_product = Product(
                product_image=product_image,
                product_description=product_description,
                product_price=product_price,
                product_quantity=product_quantity
            )
            new_product.save()

        except Exception as e:
            print(e)
            return Response(r'Erro ao adicionar o produto', status=HTTP_400_BAD_REQUEST)

        return Response('Produto adicionado com sucesso', status=HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def show_one(self, *args, **kwargs):
        products = Product.objects.all()
        value = self.request.query_params.get('value')
        value = int(value)

        product_to_show = get_object_or_404(Product, id=value)
        serializer = ProductSerializer(product_to_show)
        return Response(serializer.data, status=HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def show_all(self, request, *args, **kwargs):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    

    

   


class CartViewSet(viewsets.ViewSet):

    queryset = Product.objects.all()
    serializer_class = CartSerializer
    permission_class = (IsAuthenticated)

    def list(self, request):
        products = UserSerializer(request.user).data
        return Response(products)

    @action(detail=False, methods=['post'])
    def add_to_cart(self, *args, **kwargs):

        req = self.request.data

        user = req.get('user')
        value = self.request.query_params.get('value')
        print(value)
        product = Product.objects.get(id=value)
        user_inst = User.objects.get(username=user)

        try:

            new_buy = Cart(
                user=user_inst,
                products=product,

            )

            new_buy.save()
        except Exception as e:
            print(e)
            return Response('Não foi possível realizar a compra.', status=HTTP_400_BAD_REQUEST)

        return Response('Produto adicionado ao seu carrinho', status=HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def my_cart(self, *args, **kwargs):
        value = self.request.query_params.get('user')

        user = User.objects.get(username=value)
        user_id = user.id
        
        carts = Cart.objects.filter(user_id=user_id)

        
        produtos = []
        prod = Product.objects.get(id = 30)

        for i in carts:
            prod = Product.objects.get(id = i.products.id)
            produtos.append(prod)
        
        
        serializer = ProductSerializer(produtos, many=True)
        return Response(serializer.data, status=HTTP_200_OK)