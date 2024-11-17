from symtable import Class

from django.db import models


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

class Meal(models.Model):
    name = models.CharField(max_length=150)
    price = models.FloatField()
    out = models.CharField(max_length=10)
    image = models.ImageField(upload_to='images')
    category = models.ForeignKey(Category, default=None, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=3)

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'


    def __str__(self):
        return self.name
