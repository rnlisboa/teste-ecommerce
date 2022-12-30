from django.contrib import admin
from .models import Product, Cart
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','product_name', 'product_description', 'product_price', 'product_quantity',)
    list_display_links = ('id','product_name',)
    list_per_page = 10


admin.site.register(Product, ProductAdmin)

