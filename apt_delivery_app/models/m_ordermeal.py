from django.db import models

from .m_meal import Meal
from .m_order import Order


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