# Generated by Django 3.2.25 on 2024-11-17 18:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_cabinet'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cart',
            options={'verbose_name': 'Корзина', 'verbose_name_plural': 'Корзины'},
        ),
    ]
