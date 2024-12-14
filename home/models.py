import datetime
from symtable import Class

from django.db import models
from django.template.defaultfilters import default
from django.utils import timezone


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


class MenuDay(models.Model):
    DAYS_OF_WEEK = (
        (0, 'Понедельник'),
        (1, 'Вторник'),
        (2, 'Среда'),
        (3, 'Четверг'),
        (4, 'Пятница'),
        (5, 'Суббота'),
    )
    week_day = models.IntegerField(choices=DAYS_OF_WEEK, default=0)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Меню на день'
        verbose_name_plural = 'Меню на день'

    def __str__(self):
        return f'{self.DAYS_OF_WEEK[self.week_day][1]}'


class Menu(models.Model):
    date = models.DateTimeField(verbose_name='Дата', default=timezone.now, blank=True)

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'

    def __str__(self):
        return f'{self.date}'




