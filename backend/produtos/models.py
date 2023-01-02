from django.db import models
from django.contrib.auth.models import User
# Create your models here.

def upload_img(instance, filename):
    return f"{instance}-{filename}"

class Product(models.Model):
    product_image = models.FileField(
        upload_to=upload_img, verbose_name='Imagem')
    product_description = models.TextField(
        blank=False, null=False, verbose_name='Descrição')
    product_price = models.DecimalField(
        max_digits=9, decimal_places=2, null=False, blank=False, verbose_name='Preço unitário')
    product_quantity = models.IntegerField(blank=False,null=False,verbose_name='Quantidade')

    def image_url(self):
        return self.product_image.url


    def __str__(self):
        return self.product_description


class Cart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Usuário')
    products = models.ForeignKey(Product, on_delete= models.CASCADE,blank=False, null=False, verbose_name='Produtos')
    

    
