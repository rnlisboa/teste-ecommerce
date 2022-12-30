from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from .models import Product, Cart
from .serializers import ProductSerializer, CartSerializer, UserSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth import logout
from django.core.serializers import serialize
from django.db.models           import Q
# Create your views here.

# Cadastro e login de usuário


class UserViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request):
        user = UserSerializer(request.user).data
        return Response(user)

    @action(detail=False, methods=['post'])
    def create_user(self, *args, **kwargs):
        queryset = User.objects
        req = self.request.data

        first_name = req.get('firstname')
        username = req.get('username')
        email = req.get('username')
        password = req.get('password')

        if not (username and first_name and email and password):
            return Response(f'Preencha todos os campos.', status=400)

        try:
            user = User.objects.create(
                username=username,
                first_name=first_name,
                email=email,
                is_active=True,
                is_superuser=False
            )
            user.set_password(password)
            user.save()
        except Exception as e:
            return Response(f"Ocorreu um erro ao salvar os dados: {e}", status=400)

        return Response('Usuário salvo com sucesso.', status=200)

    @action(detail=False, methods=['post'])
    def login(self, *args, **kwargs):
        req = self.request.data

        username = req.get('username')
        password = req.get('password')

        if not (username and password):
            return Response('Preencha todos os campos.', status=400)

        user = auth.authenticate(self.request, username=username, password=password)
        print()
        if user is not None:
            auth.login(self.request, user)
            return Response('Você logou com sucesso.', status=200)
        else:
            return Response('Usuario ou senha inválido', status=400)

    @action(detail=False, methods=['post'])
    def logout(self, *args, **kwargs):
        req = self.request
        logout(req)
        return Response('Logout realizado com sucesso', status=200)


class ProductViewSet(viewsets.ViewSet):
     
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def list(self, request):
        products = UserSerializer(request.user).data
        return Response(products)

    @action(detail=False, methods=['post'])
    def add_new(self, *args, **kwargs):

        
        if not self.request.user.is_authenticated:
            return Response('Você precisa estar logado para adicionar um novo produto', status=401)
        if not self.request.user.is_superuser:
            return Response('Você não tem permissão para adicionar um novo produto', status=403)
        
        req = self.request.data
        
        product_image = req.get('product_image')
        product_name = req.get('product_name')
        product_description = req.get('product_description')
        product_price = req.get('product_price')
        product_quantity = req.get('product_quantity')
        
        if not (product_name and product_description and product_price and product_image and product_quantity):
            return Response('Todos os campos são importantes.', status=400)

        try:
            new_product = Product.objects.create(
                product_image = product_image,
                product_name = product_name,
                product_description = product_description,
                product_price = product_price,
                product_quantity = product_quantity
            )
            new_product.save()

            
        except Exception as e:
            print({e})
            return Response(r'Erro ao adicionar o produto', status = 400)
        

        return Response('Produto adicionado com sucesso', status= 200)

    @action(detail=False, methods=['get'])
    def show_one(self, *args, **kwargs):
        products = Product.objects.all()
        value = self.request.query_params.get('value')
        value = int(value)

        product_to_show = get_object_or_404(Product, id=value)
        serializer = ProductSerializer(product_to_show)
        return Response(serializer.data, status=200)
    
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
        print(product_to_update)
        print(req)
        new_product_image = req.get('product_image')
        new_product_name = req.get('product_name')
        new_product_description = req.get('product_description')
        new_product_price = req.get('product_price')
        new_product_quantity = req.get('product_quantity')
        print(len(new_product_description))
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
            return Response(r'Erro ao atualizar o produto', status = 400)
            print(e)
        return Response('Produto atualizado com sucesso.')

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
            return Response(r'Erro ao deletar o produto.', status = 400)
            
        return Response('Produto deletado com sucesso.', status=200)

    @action(detail=False, methods=['get'])
    def search(self, *args, **kwargs):
        products = Product.objects.all()
        q = self.request.query_params.get('q')
        

        found_products = products.filter(
            Q(product_name__icontains= q) |
            Q(product_description__icontains= q)
        )

        serializer = ProductSerializer(found_products, many=True)
        
        return Response(serializer.data, status=200)

    
