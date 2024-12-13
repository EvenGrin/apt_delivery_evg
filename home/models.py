import datetime
from symtable import Class

from django.db import models
from django.template.defaultfilters import default


class Category(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

class Meal(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название")
    price = models.FloatField(verbose_name="Цена")
    out = models.CharField(max_length=10, verbose_name="Выход")
    image = models.ImageField(upload_to='images', verbose_name="Изображение")
    category = models.ForeignKey(Category, default=None, on_delete=models.CASCADE,
                                 verbose_name="Категория", related_name='meals')
    quantity = models.IntegerField(default=3, verbose_name="Количество")
    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'


    def __str__(self):
        return self.name

class Menu(models.Model):
    date = models.DateTimeField(verbose_name='Дата', default=datetime.date.today)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'

    def __str__(self):
        return f'{self.date}'



