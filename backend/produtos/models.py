from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class ProdutoManager(models.Manager):
    def create(self, *args, **kwargs):
        user = kwargs.get('user', None)
        if user and user.is_authenticated and user.is_superuser:
            return super().create(*args, **kwargs)
        raise PermissionDenied

class Product(models.Model):
    product_image = models.FileField(
        upload_to=r'produtos/%Y/%m/%d/', verbose_name='Imagem')
    product_name = models.CharField(max_length=255, blank=False, null=False, verbose_name='Produto')
    product_description = models.TextField(
        blank=False, null=False, verbose_name='Descrição')
    product_price = models.DecimalField(
        max_digits=9, decimal_places=2, null=False, blank=False)
    user = models.ForeignKey(User, on_delete = models.CASCADE, blank=False, null=False, verbose_name='Usuário')

    objects = ProdutoManager()

    def __str__(self):
        return self.product_name


class Cart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Usuário')
    products = models.ManyToManyField(Product, verbose_name='Produtos')
    total_price = models.DecimalField(
        max_digits=9, decimal_places=2, verbose_name='Preço total')
