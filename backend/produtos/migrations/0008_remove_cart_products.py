# Generated by Django 4.1.4 on 2022-12-30 23:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('produtos', '0007_remove_cart_products_cart_products'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='products',
        ),
    ]