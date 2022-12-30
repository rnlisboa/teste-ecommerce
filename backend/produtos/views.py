from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from .models import Product, Cart
from .serializers import ProductSerializer, CartSerializer, UserSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout
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

        return Response('Usuário salvo com sucesso.', status = 200)

    @action(detail=False, methods=['post'])
    def login(self, *args, **kwargs):
        req = self.request.data

        username = req.get('username')
        password = req.get('password')

        if not (username and password):
            return Response('Preencha todos os campos.', status=400)
        
        user = User.authenticate(username=username, password=password)

        if user is not None: 
            return Response('Você logou com sucesso.', status=200)
        else: 
            return Response('Usuario ou senha inválido', status=400)

    @action(detail=False, methods=['post'])
    def logout(self, *args, **kwargs):
        req = self.request
        logout(req)
        return Response('Logout realizado com sucesso', status=200)

        
