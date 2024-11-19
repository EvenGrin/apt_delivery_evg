from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum

from home.models import Meal


class Status(models.Model):
    name = models.CharField(max_length=30)


    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'

    def __str__(self):
        return  self.name





class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    date_create = models.DateTimeField(verbose_name='Дата заказа', auto_now_add=True)
    status = models.ForeignKey('Status', on_delete=models.CASCADE, verbose_name='Статус', default=1)
    result = models.CharField( max_length=50, verbose_name='Причина отказа')

    @property
    def amount(self):
        return OrderMeal.objects.filter(order=self.pk).aggregate(Sum('amount'))['amount__sum']

    amount.fget.short_description = 'Количество'

    @property
    def meals(self):
        return OrderMeal.objects.filter(order=self.pk)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'покупатель: {self.user}, дата: {str(self.date_create).split(".")[0]}'


class OrderMeal(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    amount = models.IntegerField(verbose_name='Количество товаров')
    class Meta:
        verbose_name = 'Заказ блюд'
        verbose_name_plural = 'Заказы блюд'
