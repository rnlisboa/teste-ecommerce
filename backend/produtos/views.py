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

    @action(detail=False, methods=['post'])
    def logout(self, *args, **kwargs):
        req = self.request
        logout(req)
        return Response('Logout realizado com sucesso', status=HTTP_200_OK)


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

    @action(detail=False, methods=['put'])
    def update_one(self, *args, **kwargs):
        products = Product.objects.all()
        value = self.request.query_params.get('value')
        value = int(value)

        req = self.request.data

        product_to_update = get_object_or_404(Product, id=value)

        new_product_image = req.get('product_image')
        new_product_name = req.get('product_name')
        new_product_description = req.get('product_description')
        new_product_price = req.get('product_price')
        new_product_quantity = req.get('product_quantity')

        try:
            if len(new_product_image) > 0:
                product_to_update.product_image = new_product_image
            if len(new_product_name) > 0:
                product_to_update.product_name = new_product_name
            if len(new_product_description) > 0:
                product_to_update.product_description = new_product_description
            if len(new_product_price) > 0:
                product_to_update.product_price = new_product_price
            if len(new_product_quantity) > 0:
                product_to_update.product_quantity = new_product_quantity
            product_to_update.save()
        
        except Exception as e:
            return Response(r'Erro ao atualizar o produto', status=HTTP_400_BAD_REQUEST)
            print(e)
        return Response('Produto atualizado com sucesso.', HTTP_200_OK)

    @action(detail=False, methods=['delete'])
    def delete_one(self, *args, **kwargs):

        products = Product.objects.all()
        value = self.request.query_params.get('value')
        value = int(value)

        product_to_delete = get_object_or_404(Product, id=value)
        try:
            product_to_delete.delete()
        except Exception as e:
            print(e)
            return Response(r'Erro ao deletar o produto.', status=HTTP_400_BAD_REQUEST)

        return Response(status=200)

    @action(detail=False, methods=['get'])
    def search(self, *args, **kwargs):
        products = Product.objects.all()
        q = self.request.query_params.get('q')

        found_products = products.filter(
            Q(product_description__icontains=q)
        )

        serializer = ProductSerializer(found_products, many=True)

        return Response(serializer.data, status=HTTP_200_OK)


class CartViewSet(viewsets.ViewSet):

    queryset = Product.objects.all()
    serializer_class = CartSerializer
    permission_class = (IsAuthenticated)
    def list(self, request):
        products = UserSerializer(request.user).data
        return Response(products)

    @action(detail=False, methods=['post'])
    def add_to_cart(self, *args, **kwargs):
        
        value = self.request.query_params.get('value')
        if value:
            value = int(value)
        product_to_buy = get_object_or_404(Product, id=value)
        print(product_to_buy)
        
        req = self.request.data

        if not self.request.user.is_authenticated:
            return Response('Você precisa estar logado para adicionar um novo produto', status=401)
        if self.request.user.is_superuser:
            return Response('Somente cliente podem realizar pedidos.', status=403)

        user = self.request.user
        available_quantity = product_to_buy.product_quantity
        unity_price = product_to_buy.product_price

        quantity_to_buy = int(req.get('quantity'))
        unity_price = float(unity_price)
        
        if not quantity_to_buy or quantity_to_buy < 1:
            return Response('Operação inválida.', status=HTTP_400_BAD_REQUEST)
        if quantity_to_buy > available_quantity:
            return Response('Quantidade indisponível.', status=HTTP_400_BAD_REQUEST)
        
        client_user = user
        total_price_product = quantity_to_buy * unity_price

        try:
            product_to_buy.product_quantity = int(product_to_buy.product_quantity) - quantity_to_buy
            product_to_buy.save()
            new_buy = Cart.objects.create(
                user = client_user,
                products = product_to_buy,
                total_price = total_price_product,
                quantity = quantity_to_buy
            )
            
            new_buy.save()
        except Exception as e:
            print(e)
            return Response('Não foi possível realizar a compra.', status = HTTP_400_BAD_REQUEST)
        
        
        return Response('Produto adicionado ao seu carrinho', status=HTTP_200_OK)

    @action(detail=False, methods=['delete'])
    def delete_from_cart(self, *args, **kwargs):
        value = self.request.query_params.get('value')
        if value:
            value = int(value)
        product_to_delete = get_object_or_404(Cart, id=value)
        try:
            product_to_delete.delete()
        except Exception as e:
            print(e)
            return Response('Erro ao remover o produto.', status=HTTP_400_BAD_REQUEST)
        return Response(status=HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def my_cart(self, *args, **kwargs):
        
        cart = Cart.objects.all()
        
        my_cart = cart.filter(
            user = self.request.user
        )
        
        serializer = CartSerializer(my_cart, many=True)
        if len(serializer.data) < 1:
            return Response(serializer.data, status=HTTP_204_NO_CONTENT)
        return Response(serializer.data, status=HTTP_200_OK) 