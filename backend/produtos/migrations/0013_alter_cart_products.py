# Generated by Django 4.1.4 on 2023-01-02 02:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('produtos', '0012_alter_cart_products'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='products',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='produtos.product', verbose_name='Produtos'),
        ),
    ]