from decimal import Decimal

from django.conf import settings
from datetime import date, datetime
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
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

def get_default_created_at():
   return timezone.now() + timedelta(minutes=10)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    date_create = models.DateTimeField(verbose_name='Дата заказа', auto_now_add=True)
    order_date = models.DateTimeField(default=get_default_created_at, verbose_name='Дата и время получения заказа'
    )
    status = models.ForeignKey('Status', on_delete=models.CASCADE, verbose_name='Статус', default=1)
    result = models.CharField(max_length=50, verbose_name='Причина отказа', blank=True, null=True)
    cab = models.ForeignKey(Cabinet, on_delete=models.CASCADE, verbose_name='Кабинет', default=1)
    deliver = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='courier_orders',
        blank=True,
        null=True,
        limit_choices_to={'groups__name': 'deliver'},
        verbose_name="Курьер"
    )

    @property
    def total_amount(self):
        total = 0
        for item in self.ordermeal_set.all():  # ordermeal_set - обратный related_name
            total += item.meal.price * item.amount
        return total

    total_amount.fget.short_description = 'Сумма заказа'

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
        # if self.status.id == 3 and not self.result:
        #     raise ValidationError({'result': 'Обязательное поле при статусе "Отменён"'})
        # if self.status.id > 3 and self.deliver is None:
        #     raise ValidationError({'deliver': 'Укажите курьера'})
        if self.cab.id == 0 and self.deliver:
            raise ValidationError({'deliver':'К самовыносу курьер не указывается'})



    def __str__(self):
        return f'№: {self.id},\n покупатель: {self.user},\n дата: {str(self.date_create).split(".")[0]}'


class OrderMeal(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Заказ")
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, verbose_name="Блюдо")
    amount = models.IntegerField(verbose_name='Количество товаров')

    class Meta:
        verbose_name = 'Заказ блюд'
        verbose_name_plural = 'Заказы блюд'

    @property
    def total_price(self):
        return self.meal.price * self.amount

    def __str__(self):
        return f'{self.order}'
