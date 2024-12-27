from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum

from cart.models import Cabinet
from home.models import Meal
from log_reg.models import User


class Status(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    date_create = models.DateTimeField(verbose_name='Дата заказа', auto_now_add=True)
    status = models.ForeignKey('Status', on_delete=models.CASCADE, verbose_name='Статус', default=1)
    result = models.CharField(max_length=50, verbose_name='Причина отказа', blank=True, null=True)
    cab = models.ForeignKey(Cabinet, on_delete=models.CASCADE, verbose_name='Кабинет', default=1)
    courier = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='courier_orders',
        blank=True,
        null=True,
        limit_choices_to={'groups__name': 'доставщики'},
        verbose_name="Курьер"
    )

    @property
    def total_amount(self):
        total = 0
        for item in self.ordermeal_set.all():  # ordermeal_set - обратный related_name
            total += item.meal.price * item.amount
        return total

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

    def clean(self):
        if self.status.id == 3 and not self.result:
            raise ValidationError({'result': 'Обязательное поле при статусе "Отменён"'})



    def __str__(self):
        return f'покупатель: {self.user},\n дата: {str(self.date_create).split(".")[0]}'


class OrderMeal(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Заказ")
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, verbose_name="Блюдо")
    amount = models.IntegerField(verbose_name='Количество товаров')

    class Meta:
        verbose_name = 'Заказ блюд'
        verbose_name_plural = 'Заказы блюд'

    def __str__(self):
        return f'{self.order}'
